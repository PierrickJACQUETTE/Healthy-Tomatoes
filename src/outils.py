import numpy as np
import ast

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
    print(d[0].get('hits').get('hits')[i].get('_source').get('title'))
    return (s, getCast(d, si, i) + getData(d, si, i, 'genres') + getData(d, si, i, 'keywords') + getData(d, si, i, 'production_companies') + getReal(d, si, i))

def getData(d, si, a, typ) :
    text = ""
    # for i in range(si) :
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get(typ))
    for j in c :
        if(j.get('name') != None) :
            text += j.get('name')+", "
    return text

#return 3 acteurs
def getCast(d, si, a) :
    text = ""
    # for i in range(si) :
    c = ast.literal_eval(d[0].get('hits').get('hits')[a].get('_source').get('cast'))
    for j in c[:3] :
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
