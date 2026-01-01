from fastapi import FastAPI
from pydantic import BaseModel
import os


# Database emulator
users_db = {
    1: {"id": 1, "name": "Lucie", "tel": "777350949"},
    2: {"id": 2, "name": "Salamon", "tel": "777350945"}
}

PORT = os.getenv("PORT")

if not PORT:
    PORT = 5001




class User(BaseModel):
    name: str
    tel: str


app =FastAPI()

@app.get("/")
async def get_users_list():
    return {"health": "Users Service running"}, {"content": users_db}

@app.get("/{user_id}/")
async def get_user(user_id: int):
    return users_db.get(user_id, {"error": "User not found"})

@app.post("/users/add")
async def add_user(user: User):
    new_id = max(users_db.keys()) + 1
    users_db[new_id] = {"id": new_id, "name": user.name, "tel": user.tel}
    return users_db[new_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True) # type: ignore
