import operatorBDD as op
import BDD as bdd
import numpy as np
import os, sys
import pprint

#op.BDDfromCSV(sys.argv[1], bdd.tableMovieTrain, bdd.tableMovieTest, 3900)
a = op.BDDSearchAll()
# a = op.BDDSearchCategorie("title", "Avatar")
# pp = pprint.PrettyPrinter(indent=6)
# pp.pprint(a)
# print(len(a))

d = []
d.append(a)

# print(len(a))

# for i in d.keys() :
    # print(i)
# print(d)
l = []
for i in range(3898) :
    l.append(float(d[0].get('hits').get('hits')[i].get('_source').get('vote_average')))

c = 0;
for i in l :
    if(i > 6.15) :
        c += 1

print(c)

tab = np.array(l)
moy = np.mean(tab)
med = np.median(tab)
var = np.var(tab)
ect = np.std(tab, axis = 0)
print(moy, med, var, ect)




# print(d[0].get('hits').get('_source').get('vote_average'))
# print(a.vote_average)
# print(op.BDDSearchCategorie("genres", "Action"))
#print(op.BDDSearchCategorie("vote_average", "7.2"))
