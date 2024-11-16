from fastapi import FastAPI, HTTPException, Request, status
from typing import List
from models import User, Sex, Role
from uuid import UUID, uuid4
import asyncio
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

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

maintenance_mode = False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "test_user": {
        "username": "test_user",
        "password": "secret"
    }
}

def verify_credentials(username: str, password: str):
    user = fake_users_db.get(username)
    if user is None or user['password'] != password:
        raise HTTPException(status_code=401, detail="Unauthorized: Incorrect username or password")
    
    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login", status_code=203)
async def login(request: LoginRequest):
    verify_credentials(request.username, request.password)
    return {"message": "Login successful"}


# GET Method / check version checks the 

@app.get("/check-version")
async def check_version(request: Request):
    http_version = request.scope["http_version"]

    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )

    if http_version not in ["1.1", "2"]:
        raise HTTPException(
            status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
            )
    
    return {"message":"HTTP/{http_version} version is supported!"}

# GET METHOD Timeout 

@app.get("/slow")
async def slow_process(request: Request):
    try:
        await asyncio.wait_for(asyncio.sleep(10), timeout=5)
        return {"message": "Process completed successfully"}
    except asyncio.TimeoutError:
        raise HTTPException(
        status_code=status.HTTP_408_REQUEST_TIMEOUT,
        detail="Request Timeout: The request took too long to complete.")


# GET Method Gets All users


@app.get("/users")
async def fetch_users():
    if not db:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No Content"
        )
    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    return db;




#POST Method Creates a New data

@app.post("/users", status_code=201)
async def register_user(user: User):

    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    
    for existing_user in db:
        if (existing_user.first_name == user.first_name and
            existing_user.middle_name == user.middle_name and
            existing_user.last_name == user.last_name and
            existing_user.sex == user.sex and
            (existing_user.roles) == (user.roles)): 
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflict with user details"
            )
    db.append(user)
    return{"id":user.id}


#PUT Method updates an values of an existted class

@app.put("/users/{user_id}")
async def update_user(user_id: UUID, updated_user: User):

    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    
    for user in db:
        if user.id == user_id:
            user.first_name = updated_user.first_name
            user.middle_name = updated_user.middle_name
            user.last_name = updated_user.last_name
            user.sex = updated_user.sex
            user.roles = updated_user.roles
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="{user_id} Not Found!"
    )
    
#DELETE Method delets an existed class

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: UUID):

    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{user_id} Not Found!"
        )

#HEAD Method checks if the object exist

@app.head("/users/{user_id}")
async def head_user(user_id: UUID):

    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    
    for user in db:
        if user.id == user_id:
            return 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{user_id} Not Found!"
    )

# OPTIONS Method shows allowed methods

@app.options("/users/{user_id}")
async def options_user(user_id: UUID):
    if maintenance_mode:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable, there is maintenance at the server"
        )
    
    for user in db:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{user_id} Not Found!"
        )
    
    return {"allowed_methods": ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]}
