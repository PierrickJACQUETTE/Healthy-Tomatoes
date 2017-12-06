import numpy as np

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
