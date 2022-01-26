
#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Body, Query

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str 
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get('/')
def home():
    return {"Hello":"World"}

# Request and Response Body

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: Optional[int] = Query(None, ge=0, le=150)
):
    pass