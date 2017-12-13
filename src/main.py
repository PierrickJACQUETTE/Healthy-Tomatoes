## \mainpage healthy-tomatoes ocumentation
#Nous vous présentons le rapport du travail effectué dans le cadre du projet de Fouille de Données de master 2. Le projet est la réalisation d’un système de prédictions de la réussite d’un film basé sur son contenu.
#

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
matt, vect, tfidft = to.transform(lt, to.getDict(tfidf))

lt = to.createList(dt, st)

#print("MyNaiveBayes")
#al.veryNaiveBayes(lt, dic, mat, vec)

print("NaiveBayes")
print(al.naiveBayes(mat, vec, matt, vect), "%")

print("K plus proche")
x = al.find_best_k_for_kneighbors(mat, vec)
print(al.accuraccy_test(mat, vec, matt, vect, x), "%")

print("Arbre de decision / Random Forest")
al.algoTree(mat, vec, matt, vect)
