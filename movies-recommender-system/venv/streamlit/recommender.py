import streamlit as st
import pickle
import pandas
import requests
from api_key import key
st.set_page_config(layout='wide')
st.markdown(
    """
    <style>
    .appview-container {
        background-color: #2C272E;
    }
    .css-1q8dd3e{
        background-color:#3d3d3d;
        border:green solid 2px;
    }
    .css-1q8dd3e:hover{
        background-color:black;
        border:blue solid 2px;
        color:blue
    }
    .css-10trblm{
        font-size: 60px;
        text-align:center;
        background: -webkit-linear-gradient(#14C38E, #379206);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .css-14xya8e img {
        max-width:20%
    }
    </style>
    """,
    unsafe_allow_html=True
)



SimilarityScore = pickle.load(open('../../Similarity.pkl', 'rb'))

df = pickle.load(open('../../Movie_recommender.pkl', 'rb'))
df = pandas.DataFrame(df)
# print(df.head())
df_values_title = df.title.values

st.title('Movie Recommender System')
st.markdown("<center style=\"font-size:24px;\">This is a Movie recommendation system developed by Shreyas Kulkarni and Rohan Rasne of BEcomp</center>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)
st.markdown("<p>Set of Instructions to be followed</p>",unsafe_allow_html=True)
st.markdown("""
            <ul style=\"color:#14C38E"\>
                <li>The Recommendation is based on Vector Space model which employees the Cosine Similarity
                <li>The Working is simple,use the sidebar to type the movie that you want a recommendation for
                <li>Press Recommend
                <li>The recommendations for the current movie will pop up after sometime(3-4sec)
                <li>Then based on your movie knowledge compare if they are actually true!!
            </ul>
            """            ,unsafe_allow_html=True)
st.sidebar.success("Search here!")
selected_movie = st.sidebar.selectbox('Type or select a movie from the dropdown', df_values_title)


def recommender(movie_name):
    movie_index = df[df.title == movie_name].index[0]
    movie_top_10 = sorted(list(enumerate(SimilarityScore[movie_index])), reverse=True, key=lambda x: x[1])[1:10]
    recommended = []
    recommend_id = []
    recommend_poster=[]
    rec_des=[]
    rec_gen=[]

    for i in movie_top_10:
        movie_id=df.iloc[i[0]].movie_id
        recommended.append(df.iloc[i[0]].title)
        recommend_id.append(df.iloc[i[0]].movie_id)
        recommend_poster.append(fetch_data_poster(movie_id))
        rec_des.append(fetch_data_describe(movie_id))
        rec_gen.append(fetch_data_genre(movie_id))
    return recommended, recommend_poster,rec_des,rec_gen

def fetch_data_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key='+key+'&language=en-US'.format(
            movie_id))
    data = response.json()

    poster_path = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

    return poster_path

def fetch_data_describe(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key='+key+'&language=en-US'.format(
            movie_id))
    data = response.json()
    describe =  data['overview']
    return describe
    
def fetch_data_genre(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=9'+key+'&language=en-US'.format(
            movie_id))
    data = response.json()
    genres = data['genres']
    return genres


if st.sidebar.button('Recommend'):
    rec=recommender(selected_movie)
    # st.write(rec)
    recommendations,posters,describe,genres= recommender(selected_movie)
    print(describe[0],genres[0][0]['name'])

    col1, col2 = st.columns([1,1])
    
   
    for i in range(0,9):
        if i%2==0:
            col1.write(recommendations[i])
            col1.image(posters[i])
            col1.write('{}...'.format(describe[i])[:300])
            col1.write("Genre:{}".format(genres[i][0]['name']))
        else:
            col2.write(recommendations[i])
            col2.image(posters[i])
            col2.write('{}'.format(describe[i])[:300])
            col2.write("Genre:{}".format(genres[i][0]['name']))

    