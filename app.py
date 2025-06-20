import streamlit as st
import pickle
import pandas as pd
import os
import requests

# Function to download similarity.pkl from GitHub Release
def download_similarity_file():
    url = 'https://github.com/Hariom-Nagar211/Movie-Recommender-System/releases/download/v1.0/similarity.pkl'
    local_file = 'similarity.pkl'
    if not os.path.exists(local_file):
        st.write("Downloading similarity data...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

# Ensure similarity.pkl is downloaded
download_similarity_file()

# Load pickled data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox("Choose a movie", movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    st.write("### 🎥 Recommended Movies:")
    for movie in recommendations:
        st.write(f"- {movie}")
