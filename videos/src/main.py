from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
import os
import aiofiles


def view_dir(d="./video"):    
    list_ = os.listdir(d)
    vw_dr = ''
    for i in list_:
        vw_dr += f"<li><a href={i}>{i}</a></li>\n"
    
    return vw_dr

PORT = os.getenv('PORT')
if not PORT:
    PORT = 5004


app = FastAPI()

@app.get("/")
async def list_videos():
    return HTMLResponse(f"""<html><body>
        <h2 style="color: green">VIDEO STORAGE</h2>
        <hr>
        <h3>
        {view_dir()}
        </h3>
        <hr>
        <form action="/videos/upload" method="post" enctype="multipart/form-data">
        <input name="file" type="file"><button>Upload</button></form></body></html>
        <hr><hr1><form action="/"><button>TO MAIN PAGE</button></hr1></form>
        """
        )

@app.get("/{item}", response_class=StreamingResponse)
async def get_video(item: str):
    try:
        path_to_file = f"./video/{item}"
        async def stream():
            async with aiofiles.open(path_to_file, "br") as pct:
                while chunk := await pct.read(8*1024):
                    yield chunk
 
        return StreamingResponse(content=stream())
    except Exception:
        return {
            "error": 404,
            "message": "file not found",
						}
    
@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    file_name = f"./video/{file.filename}"
    async with aiofiles.open(file_name, "wb") as f:
        while True:
            chunk = await file.read(8 * 1024)
            if not chunk:
                break
            await f.write(chunk)
    return HTMLResponse(
        """<h2>File uploaded successfully</h2>
        <hr><form action="/videos"><button>BACK TO STORAGE</button></form>"""
        )

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True) 
