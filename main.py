from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pymongo import MongoClient

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = MongoClient("mongodb://localhost:27017")
db = client["api_auth"]
users_collection = db["users"]

class UserCreate(BaseModel):
    username: str
    email: str

class User(BaseModel):
    username: str
    email: str
    api_key: str
    expiry_date: datetime

def generate_api_key():
    # Generate a random 10-digit alphanumeric API key
    # Implement your own logic to generate the key
    # This is a simple example
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def encrypt_api_key(api_key):
    # Implement your own logic to encrypt the API key
    # This is a simple example using bcrypt
    return pwd_context.hash(api_key)

def verify_api_key(plain_api_key, hashed_api_key):
    # Verify the plain API key against the hashed API key
    return pwd_context.verify(plain_api_key, hashed_api_key)

@app.post("/register")
def register_user(user_create: UserCreate):
    # Create a new user with the provided data
    api_key = generate_api_key()
    hashed_api_key = encrypt_api_key(api_key)
    expiry_date = datetime.now() + timedelta(days=365)
    user = User(
        username=user_create.username,
        email=user_create.email,
        api_key=hashed_api_key,
        expiry_date=expiry_date
    )
    users_collection.insert_one(user.dict())
    return {"message": "User registered successfully","api_key":api_key}

@app.post("/user/authenticate")
def authenticate_user(api_key: str):
    # Authenticate the user based on the provided API key
    user = users_collection.find_one({"api_key": api_key})
    if user:
        return {"message": "User authenticated successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/getUserData")
def get_user_data(api_key: str):
    # Authorize the user and return user data
    user = users_collection.find_one({"api_key": api_key})
    if user:
        expiry_date = user["expiry_date"]
        if expiry_date < datetime.now():
            raise HTTPException(status_code=402, detail="API key expired")
        return {"username": user["username"], "email": user["email"]}
    else:
        raise HTTPException(status_code=400, detail="User does not exist")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
