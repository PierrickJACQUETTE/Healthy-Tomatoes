import operatorBDD as op
import BDD as bdd

import ast
import os, sys
import numpy as np
from scipy.stats import ttest_ind
from sklearn.feature_extraction.text import TfidfVectorizer

##permet de charger dans la base de donnee
def init():
    op.BDDfromCSV(sys.argv[1], sys.argv[2], bdd.tableMovieTrain, bdd.tableMovieTest)

## permet de recuperer les infos pour ensemble de train
#@return a,s,d les lignes de la base, le nombre et un dict
def getEssentialTrain() :
    a = op.BDDSearchAll();
    s = getSize(a)
    d = [a]
    return a,s,d

## permet de recuperer les infos pour ensemble de train
#@return a,s,d les lignes de la base, le nombre et un dict
def getEssentialTest():
    a = op.BDDSearchAllTest()
    s = getSize(a)
    d = [a]
    return a,s,d

##permet de savoir le nombre de hits
#@param a les lignes de la base
#@return le nombre de ligne
def getSize(a):
    return a['hits']['total']

##recuperer tous les votes
#@param d toutes les lignes
#@param si nombre de lignes
#@return a numpy array : list
def getAll_VoteAverage(d, si) :
    l = []
    for i in range(si) :
        l.append(float(d[0].get('hits').get('hits')[i].get('_source').get('vote_average')))
    return np.array(l)

## calcul des statistiques sur le champ vote_average
#@param t une ligne
#@return moyenne, median, variance, ecart de vote_average
def getData_VoteAverage(t) :
    return np.mean(t), np.median(t), np.var(t), np.std(t)

## calcul le nombre de film dont le score >= x
#@param t une ligne
#@param x number de comparaison
#@return le nombre
def ranking(t, x) :
    c = 0
    for i in t :
        if(i > x) :
            c += 1
    return c

##permet de concatener les valeurs
#@param d toutes les lignes
#@param si nombre de lignes
#@param i le numero de la ligne courante
#@returns char*
def concatData(d, si, i) :
    s = d[0].get('hits').get('hits')[i].get('_source').get('SUCCESS')
    return (s, getCast(d, si, i) + getData(d, si, i, 'genres') + getData(d, si, i, 'keywords') + getData(d, si, i, 'production_companies') + getReal(d, si, i))

##permet de contaner les valeurs dans une chaine de char
#@param d toutes les lignes
#@param si nombre de lignes
#@param a le numero de la ligne courante
#@param typ le champs a regarder
#@returns char*
def getData(d, si, a, typ) :
    text = ""
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get(typ))
    for j in c :
        if(j.get('name') != None) :
            text += j.get('name')+", "
    return text

##permet de contaner les valeurs des 6 acteurs dans une chaine de char
#@param d toutes les lignes
#@param si nombre de lignes
#@param a le numero de la ligne courante
#@return char*
def getCast(d, si, a) :
    text = ""
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get('cast'))
    for j in c[:6] :
        if(j.get('name') != None) :
            text += j.get('name')+", "
    return text

##permet de contaner les realisateurs dans une chaine de char
#@param d toutes les lignes
#@param si nombre de lignes
#@param a le numero de la ligne courante
def getReal(d, si, a) :
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get('crew'))
    for j in c :
        if (j.get('job') == "Director") and (j.get('name') != None) :
            return j.get('name')
    return "";

##liste of tuple
#@param d toutes les lignes
#@param si nombre de lignes
#@return list of tuple
def createList(d, si) :
    l = []
    for i in range(si):
        l.append(concatData(d, si, i))
    return l

## permet d'effectuer un tfidf
#@param pairs le texte
#@param vocabulary vocabulaire sur lequel applique l'algorithme
#@return tf-idf + vector
def transform(pairs, vocabulary=None):
    tfidf = TfidfVectorizer(min_df=0.005,stop_words="english",vocabulary=vocabulary,ngram_range=(1,2))
    types, text = zip(*pairs)
    matrice = tfidf.fit_transform(text)
    vector = np.array(types)
    return matrice,vector, tfidf

##permet de connaitre les labels dune tfidf
#@param tfidf ou recuperer le vocabulaire
#@return le vocabulaire de la tf-idf
def getDict(tfidf) :
    return tfidf.vocabulary_

##return an index for tfidf, None if doesn't exist
#@param dict dictionnaire
#@param s nom du labels
#@return valeur pour ce label
def getTest(dic, s):
    return dic.get(s)

## permet de savoir si cela est un succes
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@index predicat
#@return if t < 0 -> success else clear
def test_success(X, Y, index):
    X = X.toarray()
    success = X[Y == 1, index]
    failure = X[Y == 0, index]
    t, p = ttest_ind(success, failure)
    if p > 0.01 :
        return 0
    elif t < 0 :
        return -1
    else :
        return 1

## permet de calculer et d'afficher des statistiques
#@param a liste de lignes
#@return moyenne et autres stats
def stat(a):
    d = [a]
    tab = getAll_VoteAverage(d, getSize(a))
    mo, me, va, ec = getData_VoteAverage(tab)
    print("Moyenne : ", mo, " - Medianne : ", me, " - Variance : ", va, " - Ecart : ", ec)
    print("nb supérieur à moyenne : ", ranking(tab, mo))
    print("nb supérieur à mediane : ", ranking(tab, me))

##permet de creer faire des separation pour la validation croisee
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@return split
def get_train_test_sets(X, y):
    return train_test_split(X, y)
