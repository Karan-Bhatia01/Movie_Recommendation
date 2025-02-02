import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data.get("poster_path", "")

# Function to recommend movies
def recommend(movie):
    # Find the index of the movie
    movie_index = movies[movies['title'] == movie].index
    if len(movie_index) == 0:
        return [], []  # Return empty lists if movie is not found
    movie_index = movie_index[0]  # Get the actual index

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Get movie ID
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    if not names:  # Check if recommendations exist
        st.write("❌ No recommendations found. Please select a different movie.")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)  # Updated from beta_columns
        columns = [col1, col2, col3, col4, col5]

        for i in range(len(names)):
            with columns[i]:
                st.text(names[i])
                st.image(posters[i])
