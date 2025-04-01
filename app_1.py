import os
import sys
import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb
def get_path(filename): 
    if hasattr(sys, '_MEIPASS'): 
        return os.path.join(sys._MEIPASS, filename) 
    return filename 
movie = Movie()
tmdb = TMDb()
tmdb.api_key = '2e2ab0e592da871eb769e0abfa54e518'
tmdb.language = 'ko-KR'
def find_genres_movie(title_name): 
    title_moive = movies[movies['title'] == title_name] 
    title_genres = title_moive['genres'].tolist()[0] 
    temp = movies[movies['genres'].apply(lambda x : any(genres in x for genres in title_genres))] 
    temp = temp.sort_values('popularity', ascending=False).iloc[:10] 
    final_index = temp.index.values[:10] 
    images, titles = [], [] 
    for i in final_index: 
        id = movies['id'].iloc[i]
        detail = movie.details(id) 
        image_path = detail['poster_path'] 
        if image_path: 
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: 
            image_path = 'no_image.jpg' 
        images.append(image_path) 
        titles.append(detail['title']) 
    return images, titles
movies = pickle.load(open(get_path('movie_df1.pickle'), 'rb'))
st.set_page_config(layout='wide')
st.header('영화추천시스템')
movie_list = movies['title'].values
title = st.selectbox('좋아하는 영화를 입력하세요.', movie_list)
if st.button('추천'): 
    with st.spinner('로딩중...'): 
        images, titles = find_genres_movie(title)
        idx = 0 
        for i in range(0, 2): 
            cols = st.columns(5) 
            for col in cols: 
                col.image(images[idx]) 
                col.write(titles[idx]) 
                idx += 1
                