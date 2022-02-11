# Python
from uuid import UUID
from datetime import date
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr,Field

#FastAPI
from fastapi import FastAPI

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    pass

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    ),
    birth_date: Optional[date] = Field(default=None)

class Tweet():
    pass

@app.get(path='/')
def home():
    return {'Twitter API': 'Working!'}