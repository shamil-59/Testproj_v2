FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install uvicorn fastapi aiofiles httpx python-multipart

CMD ["python3", "main.py"]