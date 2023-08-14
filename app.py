import pickle
import streamlit as st
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie.append(movies.iloc[i[0]].title)
    return recommended_movie, recommended_movie_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    num_recommendations = min(len(recommended_movie_names), 5)

    if num_recommendations > 0:
        st.write("<div class='recommendations'>", unsafe_allow_html=True)
        st.write("<div class='movie-row'>", unsafe_allow_html=True)
        for movie_idx in range(num_recommendations):
            st.write("<div class='movie-card'>", unsafe_allow_html=True)
            st.image(recommended_movie_posters[movie_idx], use_column_width=True, width=20)
            st.text(recommended_movie_names[movie_idx])
            st.write("</div>", unsafe_allow_html=True)
        st.write("</div>", unsafe_allow_html=True)
        st.write("</div>", unsafe_allow_html=True)
    else:
        st.write("No recommendations available.")





