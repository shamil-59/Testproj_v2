from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Query, Depends
from fastapi.responses import JSONResponse, Response, HTMLResponse
import httpx
import os
import aiofiles
from fastapi.middleware.cors import CORSMiddleware

PORT = os.getenv("PORT")
if not PORT:
    PORT = 5000

# Database emulator
SERVICES = {
    "users":     "http://users-service:5001",
    "books":     "http://books-service:5002",
    "pictures":  "http://pictures-service:5003",
    "videos":    "http://videos-service:5004"
}


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# @app.api_route("/api/upload")

@app.get("/")
async def get_root():
    return HTMLResponse(f"""<html><body>
        <h2 style="color: green">AVAILABLE SERVICES</h2>
        <hr>
        <h3>
        <li><a href='users'>users service </a></li>
        <li><a href='books'>BOOK STORAGE</a></li>
        <li><a href='pictures'>PICTURE STORAGE</a></li>
        <li><a href='videos'>VIDEO STORAGE</a></li>
        </h3>
        <hr>
        </body></html>
        """
        )


@app.api_route("/{service}/{path:path}", methods=["GET", "POST"])
async def gateway_route(service: str, path: str, request: Request):
    # if service not in SERVICES:
    #     raise HTTPException(status_code=404, detail="Service not found")
    # print(request.headers)
    if path.strip("/") == "upload" and request.method == 'POST':
        raise HTTPException(status_code=405, detail="Use /{service}/upload endpoint for file uploads")

    target_url = f"{SERVICES[service]}/upload"

     # Forward the request
    async with httpx.AsyncClient() as client:
        body = None
        if request.method in ['POST', 'PUT']:
            body = await request.body()

            # Forward headers (excluding content-length which will be recalculated)
            headers = dict(request.headers)
            headers.pop('content-length', None)
            headers.pop("host", None)
            response = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                params=request.query_params
            )
            return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        if request.method in "GET":
            response = await client.get(f"{SERVICES[service]}/{path}")
            if service in 'users':
                    return response.json()

            else:
                return Response(content=response.content)
		

@app.post("/{service}/upload")
async def upload_file(service: str, file: UploadFile = File(...)):
    try:
        async with aiofiles.tempfile.NamedTemporaryFile('wb', delete=False) as tmpf:
            content =  file.file.read()
            await tmpf.write(content)
            tempfile_path = tmpf.name
    
        async with httpx.AsyncClient() as client:
            files = {'file': (file.filename, open(tempfile_path, "rb"), file.content_type)}
            response = await client.post(f"{SERVICES[service]}/upload", files=files)
        return  Response(content=response, status_code=response.status_code)
    finally:
        if tempfile_path and os.path.exists(tempfile_path):
            os.unlink(tempfile_path)
        file.file.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "0.0.0.0", port = int(PORT), reload=True)
