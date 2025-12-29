from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, HTMLResponse
import os
import aiofiles


def view_dir(d="./pct"):    
    list_ = os.listdir(d)
    vw_dr = ''
    for i in list_:
        vw_dr += f"<li><a href={i}>{i}</a></li>\n"
    
    return vw_dr

PORT = os.getenv('PORT')
if not PORT:
    PORT = 5003


app = FastAPI()

@app.get("/")
async def list_pictures():
    return HTMLResponse(f"""<html><body>
        <h2 style="color: green">PICTURE STORAGE</h2>
        <hr>
        <h3>
        {view_dir()}
        </h3>
        <hr><form action="/upload" method="POST" enctype="multipart/form-data">
        <input name="file" type="file"><button>Upload</button></form></body></html>
        """
        )

@app.get("/{item}")
async def get_picture(item: str):
    try:
        path_to_file = f"./pct/{item}"
        async with aiofiles.open(path_to_file, "br") as pct:
            cont = await pct.read()
        return Response(content=cont, media_type="image/jpg")

    except Exception:
        return {
            "error": 404,
            "message": "file not found"
            }

@app.post("/upload")
async def upload_picture(file: UploadFile = File(...)):   
    path_to_file = f"./pct/{file.filename}"
    print(path_to_file)
    async with aiofiles.open(path_to_file, 'wb') as f:
        await f.write(await file.read())
    return HTMLResponse(
        """<h2>File uploaded successfully</h2>
        <hr><form action="/"><button>Back to PICTURE STORAGE</button></form>"""
    )
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True) 