from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,List
import pickle
import requests
import pandas as pd

app = FastAPI()

class UserInput(BaseModel):
    movie:Annotated[str,Field(...,description='Name of the movie')]

class RecommendedMovies(BaseModel):
    movies:Annotated[List,Field(..., description='Recommended movies')]
    posters:Annotated[List,Field(..., description='Recommended movie posters')]

movies_dict = pickle.load(open('model/movies_dict.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


@app.get('/')
def home():
    return {'message': 'Movie Recommendation System'}

@app.post('/predict',response_model=RecommendedMovies)
def get_recommendation(data:UserInput):
    try:
        prediction_movie, prediction_posters = recommend(data.movie)
        return JSONResponse(status_code=200, content={'response': {'movies': prediction_movie,'posters': prediction_posters}})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))