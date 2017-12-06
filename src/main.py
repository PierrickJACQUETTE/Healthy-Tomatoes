import operatorBDD as op
import BDD as bdd
import outils as ot
import numpy as np
import os, sys
import pprint

def init():
    op.BDDfromCSV(sys.argv[1], sys.argv[2], bdd.tableMovieTrain, bdd.tableMovieTest, 3900)

def stat(a):
    d = []
    d.append(a)

    tab = ot.getAll_VoteAverage(d, a['hits']['total'])

    mo, me, va, ec = ot.getData_VoteAverage(tab)
    print(mo, me, va, ec)
    print("nb supérieur à moyenne : ", ot.ranking(tab, mo))
    print("nb supérieur à mediane : ", ot.ranking(tab, me))


#a = op.BDDSearchCategorie("genres", "Action")
# a = op.BDDSearchCategorie("title", "Avatar")
a = op.BDDSearchAll();
# pp = pprint.PrettyPrinter(indent=6)
# pp.pprint(a)
d = []
d.append(a)

for i in range(a['hits']['total']):
# for i in range(10):
    tab = ot.concatData(d, a['hits']['total'], i)
    # tab = ot.concatData(d, 10, i)
    print(tab)
    print("-------------------------")
# print(real)

#a = op.BDDSearchAll()
#stat(a)

# init()
