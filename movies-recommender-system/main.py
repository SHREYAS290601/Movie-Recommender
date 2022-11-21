import pandas as pd
import pickle as pk
df = pk.load(open('Movie_recommender.pkl', 'rb'))
df = pd.DataFrame(df)
SimilarityScore = pk.load(open('Similarity.pkl', 'rb'))
def recommender(movie_name):
    movie_index = df[df.title == movie_name].index[0]
    movie_top_10 = sorted(list(enumerate(SimilarityScore[movie_index])), reverse=True, key=lambda x: x[1])[1:10]
    distance = []
    recommended = []
    recommend_id = []
    for i in movie_top_10:
        recommended.append(df.iloc[i[0]].title)
        recommend_id.append(df.iloc[i[0]].movie_id)
        distance.append(i[1])
    return recommended, distance, recommend_id
print(recommender('Avatar'))