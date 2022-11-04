import streamlit as st
import pickle
import pandas as pd
import requests
movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
list_movies = pickle.load(open('list_movies.pkl','rb'))
def recommend(movie):
    movie_ind = movies[movies['original_title'] == movie].index[0]
    # distance = similarity[movie_ind] sorted(list(enumerate(distance)), reverse=-1, key=lambda x: x[1])
    recomdded_movies = list_movies[movie_ind][0:10]
    movie_list=[]
    release = []
    overview = []
    genres = []
    production_com = []
    poster=[]
    for i in recomdded_movies:
        movie_id=movies.iloc[i[0]].id
        movie_list.append(movies.iloc[i[0]].original_title)
        release.append(movies.iloc[i[0]].release_date)
        overview.append(movies.iloc[i[0]].overview)
        genres.append(movies.iloc[i[0]].genres)
        production_com.append(movies.iloc[i[0]].production_companies)
        responce = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=2ea0429a3f4de0f5b90e7cd63c01bf86&language=en-US'.format(
                movie_id))
        data=responce.json()
        poster.append("https://image.tmdb.org/t/p/w500/" + data['poster_path'])
    return movie_list,release,overview,genres,production_com,poster

st.title("Movie recommendation system ")
selected_movie = st.selectbox('Enter Movie Name here: ',movies['original_title'].values)
if st.button('Recommend'):
    recommendation,release,overview,genres,production_com,posters =recommend(selected_movie)
    for i in range(9):
        col1,col2 = st.columns([1,4])
        with col1:
            st.image(posters[i],use_column_width=True)
        with col2:
            st.subheader(recommendation[i])
            st.text(f"release date: {release[i]}")
            gen = ", ".join(genres[i])
            st.text(f"Genres: {gen}")
            com = ", ".join(production_com[i])
            st.text(f"Production Companies: {com}")
            st.markdown(overview[i])
