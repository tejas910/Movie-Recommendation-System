import streamlit as st
import pickle
import pandas as pd
import requests
movies_list = pickle.load(open('movies_dict.pkl','rb'))

def fectch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie = []
    recommended_movie_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie.append(movies.iloc[i[0]].title)
        #fetch poster api
        recommended_movie_poster.append(fectch_poster(movie_id))
    return recommended_movie,recommended_movie_poster

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Hey Buddy Go there I will recommend you movie',movies['title'].values)

if st.button('Recommend'):
    recommendation,poster = recommend(selected_movie_name)
    col1, col2, col3,col4, col5 = st.columns(5)
    with col1:
        st.text(recommendation[0])
        st.image(poster[0])
    with col2:
        st.text(recommendation[1])
        st.image(poster[1])
    with col3:
        st.text(recommendation[2])
        st.image(poster[2])
    with col4:
        st.text(recommendation[3])
        st.image(poster[3])
    with col5:
        st.text(recommendation[4])
        st.image(poster[4])

