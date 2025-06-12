import streamlit as st
from frontend.list import movie_list
import requests

API_URL = "http://backend:8000/predict"

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    try:
        response = requests.post(API_URL, json={"movie": selected_movie})
        if response.status_code == 200:
            result = response.json()
            movies = result['response']['movies']
            posters = result['response']['posters']

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(movies[0])
                st.image(posters[0])
            with col2:
                st.text(movies[1])
                st.image(posters[1])
            with col3:
                st.text(movies[2])
                st.image(posters[2])
            with col4:
                st.text(movies[3])
                st.image(posters[3])
            with col5:
                st.text(movies[4])
                st.image(posters[4])
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")



