
#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field

from fastapi import FastAPI,status,Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Location(BaseModel):
    city: str
    state: str
    country: str


class PersonBase(BaseModel):
    first_name: str = Field(
            ...,
            min_length=1,
            max_length=50,
            example='Facundo'
        )
    last_name: str = Field(
            ...,
            min_length=1,
            max_length=50,
            example='García Martoni'
        )
    age: int = Field(
            ...,
            gt=0,
            le=115,
            example=25
        )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)

class PersonOut(PersonBase):
    pass


class Person(PersonBase):
    password: str = Field(...,min_length=8)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             'first_name': 'Facundo',
    #             'last_name': 'García Martoni',
    #             'age':21,
    #             'hair_color': 'blonde',
    #             'is_married': False
    #         }
    #     }


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {'Hello':'World'}

# Request and Response Body

@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description="This is the person name. It's between 1 and 50 characters.",
        example='Rocío'),
    age: Optional[int] = Query(
        None,
        ge=0,
        le=150,
        title='Person Age',
        description="This is the person age. It's required",
        example=25
        )
):
    return {name: age}

#Validations: Path Parameters

@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        ge=1,
        title='Person Id',
        description="This is the person id. It's greated or equals than 1",
        example=123
        )
    ):
    return {person_id: 'It exists!'}


#Validations: Request Body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person Id',
        description='This is the person id.',
        ge=1,
        example=123
    ),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())

    return person
