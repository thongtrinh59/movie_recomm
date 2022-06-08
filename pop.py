import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from ast import literal_eval


def popular_rec():
    credits = pd.read_csv('tmdb_5000_credits.csv')
    movies = pd.read_csv('tmdb_5000_movies.csv')

    credits = credits.rename(columns = {'movie_id': 'id'})
    imdb = movies.merge(credits, on='id')


    imdb = imdb.drop(['homepage','production_countries','release_date','status','tagline','title_x','title_y'],axis=1)

    v = imdb['vote_count']
    R = imdb['vote_average']
    C = imdb['vote_average'].mean()
    m = imdb['vote_count'].quantile(0.8)

    imdb['weighted_average'] = ((R * v) + (C * m)) / (v + m)

    imdb.sort_values('weighted_average',ascending=False)[['original_title', 'vote_count', 'vote_average', 'weighted_average', 'popularity']].head(20)



    scaling=MinMaxScaler()
    scaled_imdb=scaling.fit_transform(imdb[['weighted_average','popularity']])
    normalized_imdb=pd.DataFrame(scaled_imdb,columns=['weighted_average','popularity'])

    imdb[['normalized_weight_average','normalized_popularity']]= normalized_imdb

    imdb['score'] = imdb['normalized_weight_average'] * 0.5 + imdb['normalized_popularity'] * 0.5
    result = imdb.sort_values(['score'], ascending=False)[['original_title', 'normalized_weight_average', 'normalized_popularity', 'score']].head(20)

    metadata = pd.read_csv('movies_metadata.csv', dtype={"overview": "string", "popularity": "string"})

    result = result.merge(metadata, on='original_title')

    finalresult = pd.DataFrame(result, columns= ['original_title', 'imdb_id', 'runtime', 'release_date', 'vote_average'])

    finalresult = finalresult.drop_duplicates(['original_title'])

    templ = finalresult.values.tolist()

    return templ