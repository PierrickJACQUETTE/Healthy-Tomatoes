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

a = op.BDDSearchAll();
s = to.getSize(a)
# pp = pprint.PrettyPrinter(indent=6)
# pp.pprint(a)
d = []
d.append(a)

# init()
# stat(a)

l = to.createList(d, s)

mat, vec, tfidf = to.transform(l)

dic = to.getDict(tfidf)

test = op.BDDSearchAllTest()
st = to.getSize(test)

dt = []
dt.append(test)

lt = to.createList(dt, st)

true = fail = 0

for (i,j) in lt :
    res = per = 0;
    sp = j.split()
    for k in sp :
        k = k.replace(',', '').lower()
        bob = to.getTest(dic, k)
        if(bob != None) :
            res += to.test_success2(mat, vec, bob)
        else :
            per += 1
    print(i, res, per)
    if(i == 1 and res >= 0) :
        true += 1
    elif (i == 0 and res < 0) :
        true += 1
    else :
        fail += 1

print("OK : ", true)
print("KO : ", fail)
