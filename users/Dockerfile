FROM python:3.11-slim

WORKDIR /app
COPY ./src ./src
RUN pip install --upgrade pip
RUN pip install uvicorn fastapi pydantic

CMD ["python3", "src/main.py"]