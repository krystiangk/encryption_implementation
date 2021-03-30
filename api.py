from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from functools import wraps
from typing import Optional
import secrets
from rsa import key_generation, encrypt, decrypt
from models import User
import schemas
from sqlalchemy.orm import Session
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        correct_password = secrets.compare_digest(credentials.password, db.get(credentials.username).password)
    except AttributeError:
        correct_password = False

    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/register/")
def register(db: Session, user: schemas.RegisterUser):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db


@app.post("/encrypt")
def encryption(data: schemas.EncryptMsg, username: str = Depends(authenticate)):
    _id, *pk = list(map(lambda x: int(x), data.public_key.split('b')))
    encrypted_msg = encrypt(tuple(pk), data.message)
    return {"Encrypted message": "e".join([str(num) for num in encrypted_msg])}


@app.post("/decrypt")
def decryption(db:Session, message: schemas.DecryptMsg, username: str = Depends(authenticate)):
    cleaned_msg = [int(string) for string in str(message).split("e")]
    user = db.query(models.User).filter(models.User.username == username).first()
    pk = user.private_key
    print(pk)
    print(username)

    decrypted_msg = decrypt(pk, cleaned_msg)
    return {"Decrypted message": decrypted_msg}


@app.get("/generate_keys")
def generate_keys(db: Session, username: str = Depends(authenticate)):
    User("krystian@gmail.com", "pass1")
    public, private = key_generation()
    user = db.query(models.User).filter(models.User.username == username).first()
    mod_public = f"{user.id}b{public[0]}b{public[1]}"
    user.set_keys(mod_public, private)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"Your public Key": mod_public}


SQL_ALCHEMY_DATABASE_URI = 'sqlite///db.sqlite3'

"username: str = Depends(authenticate),"






