from typing import List, Optional
from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True

class DirectorBase(BaseModel):
    name: str

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int

    class Config:
        orm_mode = True

class ActorBase(BaseModel):
    name: str

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    description: str
    release_year: int

class MovieCreate(MovieBase):
    director_id: int
    actor_ids: List[int]
    genre_ids: List[int]

class Movie(MovieBase):
    id: int
    director: Director
    actors: List[Actor]
    genres: List[Genre]
    average_rating: Optional[float] = None

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class RatingBase(BaseModel):
    score: float

class RatingCreate(RatingBase):
    user_id: int
    movie_id: int

class Rating(RatingBase):
    id: int
    user: User
    movie: Movie

    class Config:
        orm_mode = True

class ViewingCreate(BaseModel):
    user_id: int
    movie_id: int

class Viewing(BaseModel):
    id: int
    user: User
    movie: Movie

    class Config:
        orm_mode = True

class MovieRecommendation(BaseModel):
    movie: Movie
    similarity_score: float