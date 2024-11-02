from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Sex, Role
from uuid import UUID, uuid4

app = FastAPI()


db: List[User] = [
    User(
        id=UUID("62c2f1ab-1669-4299-a3f8-cb8b73db2965"),
        first_name= "Metehan",
        last_name = "Kilicli",
        sex = Sex.male,
        roles = [Role.admin, Role.student]
       ),

    User(
        id=UUID("2fdb86b4-ccbe-4cf1-96e7-573d9f416be4"),
        first_name= "Ahsen",
        last_name = "Cenberci",
        sex = Sex.female,
        roles = [Role.user, Role.student]
       ),

       User(
        id=UUID("f1b04650-cd51-4d10-9c07-9f4036569eae"),
        first_name= "Celal",
        middle_name = "Kaan",
        last_name = "Yalcin",
        sex = Sex.male,
        roles = [Role.user, Role.student]
       ),

       User(
        id=UUID("33769f39-7468-4d0e-ad53-7e73d77483b0"),
        first_name= "Serpil",
        middle_name= "Duru",
        last_name = "Mert",
        sex = Sex.female,
        roles = [Role.admin, Role.student]
       )

]

# GET Method Gets All users

@app.get("/users")
async def fetch_users():
    return db;

#Post Method Posts New Object

@app.post("/users")
async def register_user(user: User):
    db.append(user)
    return{"id": user.id}

#PUT Methods updates a existted value

@app.put("/users/{user_id}")
async def update_user(user_id: UUID, updated_user: User):

    for user in db:
        if user.id == user_id:
            user.first_name = updated_user.first_name
            user.middle_name = updated_user.middle_name
            user.last_name = updated_user.last_name
            user.sex = updated_user.sex
            user.roles = updated_user.roles
            return user
        raise HTTPException(
            status_code=404,
            detail="{user_id} Not Found!"
        )
    
#DELETE Methode Delets a existed class

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        raise HTTPException(
            status_code=404,
            detail="{user_id} Not Found!"
        )

#HEAD Method Checks if the object exist

@app.head("/users/{user_id}")
async def head_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return 
    raise HTTPException(
        status_code=404,
        detail=f"{user_id} Not Found!"
    )

# OPTIONS Method shows allowed methods

@app.options("/users/{user_id}")
async def options_user(user_id: UUID):
    return {"allowed_methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]}