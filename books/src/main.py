from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, HTMLResponse
import aiofiles
import os


def view_dir(d="./book"):    
    list_ = os.listdir(d)
    vw_dr = ''
    for i in list_:
        vw_dr += f"<li><a href={i}>{i}</a></li>\n"
    
    return vw_dr

PORT = os.getenv('PORT')
if not PORT:
    PORT = 5002


app = FastAPI()

@app.get("/")
async def list_books():
    return HTMLResponse(f"""
        <html><body>
        <h2 style="color: green">BOOKS STORAGE</h2>
        <hr>
        <h3>
        {view_dir()}
        </h3>
        <hr>
        <form action="/upload" method="post" enctype="multipart/form-data">
        <input name="file" type="file"><button>Upload</button></form></body></html>
        """
        )

@app.get("/{book_name}")
async def get_book(book_name: str):
    try:
        path_to_file = f"./book/{book_name}"
        print(path_to_file)
        async with aiofiles.open(path_to_file, 'rb') as book:
            resp = await book.read()
        return Response(resp)

    except Exception:
        return {"error": "Book not found"}


@app.post("/upload")
async def upload_book(file: UploadFile = File(...)):
    file_name = f"./books/book/{file.filename}"
    async with aiofiles.open(file_name, "wb") as f:
        await f.write(await file.read())
    return HTMLResponse(
        """<h2>File uploaded successfully</h2>
        <hr><form action="/"><button>Back to BOOKS STORAGE</button></form>"""
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True)