import algo as al
import BDD as bdd
import toolsBDD as to
import operatorBDD as op

# Lecture des .csv pour remplire la BDD
# to.init()

a,s,d = to.getEssentialTrain()
to.stat(a)

l = to.createList(d, s)
mat, vec, tfidf = to.transform(l)
dic = to.getDict(tfidf)

test,st,dt = to.getEssentialTest()
lt = to.createList(dt, st)

print("naiveBayes")
al.naiveBayes(lt, dic, mat, vec)

print("K plus proche")
x = al.find_best_k_for_kneighbors(mat, vec)
print(al.accuraccy_test(mat, vec, tfidf, lt, x), "%")

print("Arbre de decision / Random Forest")
al.algoTree(mat, vec, tfidf, lt)
