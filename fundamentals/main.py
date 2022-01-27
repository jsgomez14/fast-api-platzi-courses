
#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Location(BaseModel):
    city: str
    state: str
    country: str

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
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description="This is the person name. It's between 1 and 50 characters."),
    age: Optional[int] = Query(
        None,
        ge=0,
        le=150,
        title='Person Age',
        description="This is the person age. It's required"
        )
):
    return {name: age}

#Validations: Path Parameters

@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        ge=1,
        title="Person Id",
        description="This is the person id. It's greated or equals than 1"
        )
    ):
    return {person_id: "It exists!"}


#Validations: Request Body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person Id',
        description="This is the person id.",
        ge=1
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results
