import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

metdat = pd.read_csv('movies_metadata.csv', dtype={"overview": "string", "popularity": "string"})
crd = pd.read_csv('credits.csv')
kw = pd.read_csv('keywords.csv')

metdat = metdat.iloc[0:5000,:]
crd = crd.iloc[0:5000,:]
kw = kw.iloc[0:5000,:]

kw['id'] = kw['id'].astype('int')
crd['id'] = crd['id'].astype('int')
metdat['id'] = metdat['id'].astype('int')


metdat = metdat.merge(crd, on='id')
metdat = metdat.merge(kw, on='id')

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    metdat[feature] = metdat[feature].apply(literal_eval)


def GetDir(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

metdat['director'] = metdat['crew'].apply(GetDir)


def GetLi(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []


features = ['cast', 'keywords', 'genres']
for feature in features:
    metdat[feature] = metdat[feature].apply(GetLi)


def CleanDat(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    metdat[feature] = metdat[feature].apply(CleanDat)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])


metdat['soup'] = metdat.apply(create_soup, axis=1)


def make_recommendation(query, metadata=metdat):
	new_row = metadata.iloc[-1,:].copy()

	new_row.iloc[-1] = query

	metadata = metadata.append(new_row)

	count = CountVectorizer(stop_words='english')
	count_matrix = count.fit_transform(metadata['soup'])

	cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

	sim_scores = list(enumerate(cosine_sim2[-1,:]))
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

	ranked_titles = []
	for i in range(1, 11):
		indx = sim_scores[i][0]
		ranked_titles.append([metadata['title'].iloc[indx], metadata['imdb_id'].iloc[indx], metadata['runtime'].iloc[indx], metadata['release_date'].iloc[indx], metadata['vote_average'].iloc[indx]])

	return ranked_titles


# query = "horror jameswan dreadful"

# make_recommendation(query, metadata)