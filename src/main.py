import operatorBDD as op
import BDD as bdd
import toolsBDD as to
import numpy as np
import os, sys
import pprint

def init():
    op.BDDfromCSV(sys.argv[1], sys.argv[2], bdd.tableMovieTrain, bdd.tableMovieTest, 3900)

def stat(a):
    d = [a]
    tab = to.getAll_VoteAverage(d, to.getSize(a))
    mo, me, va, ec = to.getData_VoteAverage(tab)
    print(mo, me, va, ec)
    print("nb supérieur à moyenne : ", to.ranking(tab, mo))
    print("nb supérieur à mediane : ", to.ranking(tab, me))


#a = op.BDDSearchCategorie("genres", "Action")
# a = op.BDDSearchCategorie("title", "Avatar")
a = op.BDDSearchAll();
s = to.getSize(a)
# pp = pprint.PrettyPrinter(indent=6)
# pp.pprint(a)
d = []
d.append(a)

# init()
# stat(a)

l = to.createList(d, s)
print("List done")

mat, vec, tfifdf = to.transform(l)
print("matrice + vector done")

dic = tfifdf.vocabulary_
test_freeman = dic.get('freeman')
print(to.test_success(mat, vec, test_freeman))
