import streamlit  as st
import pandas as pd
import requests
import pickle


with open('movie_data.pkl','rb') as file:
    movies, cosine_sim = pickle.load(file)


def get_recommend(title, cosine_sim= cosine_sim):
    idx = movies[movies['title']== title].index[0]
    sim_score = list(enumerate(cosine_sim[idx]))
    sim_score = sorted(sim_score, key= lambda x: x[1], reverse=True)
    sim_score = sim_score[1:11]   #Get top 10 similar movies
    movie_indices = [i[0] for i in sim_score]
    return movies.iloc[movie_indices][['title', 'movie_id']]


def fetch_poster(movie_id):
    api_key = 'e45bb0333b9c70bf7b66368901447180'  
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

# Streamlit UI
st.title("Movie Recommendation System")
selected_movie = st.selectbox("select a movie: ", movies["title"].values)

if st.button('Recommend'):
    recommendations = get_recommend(selected_movie)
    st.write("Top 10 recommended movies")

# create 2*5 grid

    for i in range(0,10,5) :#(2 rows for 5 outputs)
        cols = st.columns(5) #5 col for each row 
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]["title"]
                movie_id = recommendations.iloc[j]["movie_id"]
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)
