FROM python:3.11-slim

WORKDIR /app
COPY ./src ./src
COPY ./video ./video
RUN pip install --upgrade pip
RUN pip install uvicorn fastapi aiofiles python-multipart

CMD ["python3", "src/main.py"]