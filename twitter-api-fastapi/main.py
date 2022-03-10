# Python
import json
from uuid import UUID
from datetime import date,datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr,Field

#FastAPI
from fastapi import Body, FastAPI, status

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserSignup(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

## Users

### User signup
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register an User',
    tags=['Users']
)
def signup(user: UserSignup = Body(...)):
    """
    Signup

    This path operation creates a user in the app.

    Parameters:
        - Request Body parameter
            - user: UserSignup
    
    Returns a json with the basic user information:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open('users.json','r+',encoding='utf-8') as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### User login
@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login an User',
    tags=['Users']
)
def login():
    pass

### Show all users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all Users',
    tags=['Users']
)
def show_all_users():
    """
    This path operation shows all users in the app.

    Parameters:
        -

    Returns a json list with all users in the app, with the following keys:
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results

### Show an user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show an User',
    tags=['Users']
)
def show_user():
    pass

### Delete an user
@app.delete(
    path='/users/{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Delete an User',
    tags=['Users']
)
def delete_user():
    pass

### Update an user
@app.put(
    path='/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update an User',
    tags=['Users']
)
def update_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Show all Tweets',
    tags=['Tweets']
    )
def home():
    return {'Twitter API': 'Working!'}

### Show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a Tweet',
    tags=['Tweets']
)
def show_tweet():
    pass

### Post a tweet
@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Post a Tweet',
    tags=['Tweets']
)
def post():
    pass

### Delete a tweet
@app.delete(
    path='/tweets/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Delete a Tweet',
    tags=['Tweets']
)
def delete_tweet():
    pass

### Update a tweet
@app.delete(
    path='/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Update a Tweet',
    tags=['Tweets']
)
def update_tweet():
    pass




