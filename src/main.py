import operatorBDD as op
import BDD as bdd
import outils as ot
import numpy as np
import os, sys
import pprint

def init():
    op.BDDfromCSV(sys.argv[1], bdd.tableMovieTrain, bdd.tableMovieTest, 3900)

def stat(a):
    d = []
    d.append(a)

    tab = ot.getAll_VoteAverage(d, a['hits']['total'])

    mo, me, va, ec = ot.getData_VoteAverage(tab)
    print(mo, me, va, ec)
    print("nb supérieur à moyenne : ", ot.ranking(tab, mo))
    print("nb supérieur à mediane : ", ot.ranking(tab, me))


# a = op.BDDSearchCategorie("title", "Avatar")
# a = op.BDDSearchCategorie("genres", "Action")
# a = op.BDDSearchCategorie("vote_average", "7.2")

# pp = pprint.PrettyPrinter(indent=6)
# pp.pprint(a)

a = op.BDDSearchAll()
stat(a)
