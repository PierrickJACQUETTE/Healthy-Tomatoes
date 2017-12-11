import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import ttest_ind

def getSize(a):
    return a['hits']['total']

#return a numpy array : list
def getAll_VoteAverage(d, si) :
    l = []
    for i in range(si) :
        l.append(float(d[0].get('hits').get('hits')[i].get('_source').get('vote_average')))
    return np.array(l)

#return moyenne, median, variance, ecart de vote_average
def getData_VoteAverage(t) :
    return np.mean(t), np.median(t), np.var(t), np.std(t)

#return nb de film dont le score >= x
def ranking(t, x) :
    c = 0
    for i in t :
        if(i > x) :
            c += 1
    return c

def concatData(d, si, i) :
    s = d[0].get('hits').get('hits')[i].get('_source').get('SUCCESS')
    # print(d[0].get('hits').get('hits')[i].get('_source').get('title'))
    return (s, getCast(d, si, i) + getData(d, si, i, 'genres') + getData(d, si, i, 'keywords') + getData(d, si, i, 'production_companies') + getReal(d, si, i))

def getData(d, si, a, typ) :
    text = ""
    # for i in range(si) :
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get(typ))
    for j in c :
        if(j.get('name') != None) :
            text += j.get('name')+", "
    return text

#return 6 acteurs
def getCast(d, si, a) :
    text = ""
    # for i in range(si) :
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get('cast'))
    for j in c[:6] :
        if(j.get('name') != None) :
            text += j.get('name')+", "
    return text

#return realisateur
def getReal(d, si, a) :
    # for i in range(si) :
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get('crew'))
    for j in c :
        if (j.get('job') == "Director") and (j.get('name') != None) :
            return j.get('name')
    return "";

#liste of tuple
def createList(d, si) :
    l = []
    for i in range(si):
        l.append(concatData(d, si, i))
    return l

#return tf-idf + vector
def transform(pairs, vocabulary=None):
    tfidf = TfidfVectorizer(min_df=0.005,stop_words="english",vocabulary=vocabulary)
    types, text = zip(*pairs)
    matrice = tfidf.fit_transform(text)
    vector = np.array(types)
    return matrice,vector, tfidf

def getDict(tfidf) :
    return tfidf.vocabulary_

#return an index for tfidf, None if doesn't exist
def getTest(dic, s):
    return dic.get(s)

#if t < 0 -> success else clear
def test_success(X, Y, index):
    X = X.toarray()
    success = X[Y == 1, index]
    failure = X[Y == 0, index]
    t, p = ttest_ind(success, failure)
    return t, p

#if t < 0 -> success else clear
def test_success2(X, Y, index):
    X = X.toarray()
    success = X[Y == 1, index]
    failure = X[Y == 0, index]
    t, p = ttest_ind(success, failure)
    if p > 0.1 :
        return 0
    elif t < 0 :
        return -1
    else :
        return 1
