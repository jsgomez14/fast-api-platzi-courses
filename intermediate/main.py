#Python
from importlib.resources import path
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import  FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import  Query, Path, Body,Form, Header, Cookie,UploadFile,File

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

class Person(PersonBase):
    password: str = Field(...,min_length=8)
class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example='miguel2021')

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
    status_code=status.HTTP_200_OK,
    tags=['Home']
    )
def home():
    return {'Hello':'World'}

# Request and Response Body

@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['People'],
    summary='Create Person in the app'
    )
def create_person(person: Person = Body(...)):
    """Create Person
       
       This path operation creates a person in the app and save the information in the database.
    Args:
    - Request body parameter
        - **person (Person, mandatory):** A person model with first name, last name, age, hair color and marital status.

    Returns:
        **person (Person)** : person model with first name, last name, age, hair color and marital status.
    """
    return person

# Validations: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['People'],
    deprecated=True,
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
PEOPLE = [1,2,3,4,5]

@app.get('/person/detail/{person_id}',tags=['People'])
def show_person(
    person_id: int = Path(
        ...,
        ge=1,
        title='Person Id',
        description="This is the person id. It's greated or equals than 1",
        example=123
        )
    ):
    if person_id not in PEOPLE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This person doesn\'t exists'
        )
    return {person_id: 'It exists!'}


#Validations: Request Body

@app.put('/person/{person_id}',tags=['People'])
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


@app.post(
        path='/login',
        response_model=LoginOut,
        status_code=status.HTTP_200_OK,
        tags=['People','Auth']
    )
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


# Cookies and Headers Parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contacts']
)
def contact(
    first_name: str = Form(
            ...,
            max_length=20,
            min_length=1
        ),
    last_name: str = Form(
            ...,
            max_length=20,
            min_length=1
        ),
    email: EmailStr = Form(...),
    message: str = Form(
            ...,
            min_length=20
        ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

#files

@app.post(
    path= '/post-image',
    tags = ['Files']
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read())/1024, ndigits=2)
    }