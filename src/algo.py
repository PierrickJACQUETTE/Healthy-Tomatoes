import operatorBDD as op
import toolsBDD as to

import os, sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##permet de savoir si c'est un echec ou succes
#@param lt list de tuples contenant (success, puis liste de mot)
#@param dic dictionnaire de la tfdif
#@param mat resultat de la tfidf
#@param vec vecteur de la tfidf
#
def veryNaiveBayes(lt, dic, mat, vec) :
    true = fail = 0

    for (i,j) in lt :
        res = per = 0;
        sp = j.split()
        for k in sp :
            k = k.replace(',', '').lower()
            bob = to.getTest(dic, k)
            if(bob != None) :
                res += to.test_success(mat, vec, bob)
            else :
                per += 1
        # print(i, res, per)
        if(i == 1 and res >= 0) :
            true += 1
        elif (i == 0 and res < 0) :
            true += 1
        else :
            fail += 1

    print("OK : ", true)
    print("KO : ", fail)

##permet de savoir si c'est un echec ou succes
#@param mat resultat de la tfidf de train
#@param vec vecteur de la tfidf de train
#@param matt resultat de la tfidf de test
#@param vect vecteur de la tfidf de test
#@return score en pourcentage sur l'ensemble de test
#
def naiveBayes(mat, vec, matt, vect):
    model = BernoulliNB()
    model.fit(mat,vec)
    y_pred =model.predict(matt)
    print("Precision ", precision_score(vect, y_pred, average='macro')*100, "% et Recall", recall_score(vect, y_pred, average='macro')*100, "%")
    return model.score(matt, vect)*100


##permet de savoir le meilleur k possible
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@param n_splits, combien de sous ensemble pour la validation croisee
#@param show savoir si l'on dessine le graph
#@return best k
#
def find_best_k_for_kneighbors(X, y, n_splits=5, show=0):
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    skf = StratifiedKFold(n_splits=n_splits)

    best_k = 1
    best_score = 0
    k_range = range(1, 100, 2)
    scores = []
    for k in k_range:
        score_sum = 0.0

        for train_idx, test_idx in skf.split(X_train, y_train):
            X_subtrain, X_subtest = X[train_idx], X[test_idx]
            y_subtrain, y_subtest = y[train_idx], y[test_idx]

            model = KNeighborsClassifier(k, n_jobs=-1).fit(X_subtrain, y_subtrain)
            score = model.score(X_subtest, y_subtest)

            score_sum += score

        score_sum /= n_splits
        scores.append(score_sum)
        if score_sum > best_score:
            best_score = score_sum
            best_k = k
    if(show==1):
        plt.plot(k_range, scores)
        plt.xlabel('Value of K for KNN')
        plt.ylabel('Testing Accuracy')
        plt.show()
    return best_k

##permet de savoir si c'est un echec ou succes
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@param k nombre de k voisin
#@param matt resultat de la tfidf de test
#@param vect vecteur de la tfidf de test
#@return score en pourcentage sur l'ensemble de test
#
def accuraccy_test(X, y, matt, vect, k=77):
    knn = KNeighborsClassifier(k, n_jobs=-1)
    knn.fit(X, y)
    y_pred =knn.predict(matt)
    print("Precision ", precision_score(vect, y_pred, average='macro')*100, "% et Recall", recall_score(vect, y_pred, average='macro')*100, "%")
    score = knn.score(matt, vect)
    return score*100

##permet de savoir les meilleurs parametres
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@param cls fonction
#@param show savoir si l'on dessine le graph
#@return best_min_samples_split,best_max_depth parametres optimaux
#
def generic_tree(X, y, cls, show=0):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits)
    best_min_samples_split = 2
    best_max_depth = None
    best_score = 0
    tab_max_depths = []
    tab_min_samples_split = []
    scores = []
    for min_samples_split in range(2, 22):
        for max_depth in range(2, 22):
            score_sum = 0.0
            for train_idx, test_idx in skf.split(X_train, y_train):
                X_sub_train, X_sub_test = X[train_idx], X[test_idx]
                y_sub_train, y_sub_test = y[train_idx], y[test_idx]
                if(cls==DecisionTreeClassifier):
                    model = cls(min_samples_split=min_samples_split, max_depth=max_depth)
                else:
                    model = cls(min_samples_split=min_samples_split, max_depth=max_depth, n_jobs=-1, n_estimator=1000)
                model.fit(X_sub_train, y_sub_train)
                score = model.score(X_sub_test, y_sub_test)
                score_sum += score
                score_average = score_sum / n_splits
            scores.append(score_average)
            tab_max_depths.append(max_depth)
            tab_min_samples_split.append(min_samples_split)
            if score_average > best_score:
                best_score = score_average
                best_min_samples_split = min_samples_split
                best_max_depth = max_depth

    if(show == 1):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(tab_max_depths, tab_min_samples_split, scores, c='r', marker='o')
        ax.set_xlabel('Value of max_depths')
        ax.set_ylabel('Value of min_samples_split')
        ax.set_zlabel('Testing Accuracy')
        plt.show()

    return best_min_samples_split, best_max_depth

##permet de savoir si c'est un echec ou succes
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@param matt resultat de la tfidf de test
#@param vect vecteur de la tfidf de test
#@param show savoir si l'on dessine le graph
#@return score en  pourcentage
#
def generic_tree_score(X, y, matt, vect, cls, show=0):
    best_min, best_max = generic_tree(X, y, cls, show)
    if(cls==DecisionTreeClassifier):
        m = cls(min_samples_split=best_min, max_depth=best_max)
    else:
        m = cls(min_samples_split=best_min, max_depth=best_max, n_jobs=-1, n_estimator=1000)
    m.fit(X, y)
    y_pred =m.predict(matt)
    print("Precision ", precision_score(vect, y_pred, average='macro')*100, "% et Recall", recall_score(vect, y_pred, average='macro')*100, "%")

    score = m.score(matt, vect)
    return score

##permet de lancer pour les deux arbres
#@param X resultat de la tfidf
#@param y vecteur de la tfidf
#@param matt resultat de la tfidf de test
#@param vect vecteur de la tfidf de test
#@param show savoir si l'on dessine le graph
#
def algoTree(X, y, matt, vect, show=0):
    tree_score = generic_tree_score(X, y, matt, vect, DecisionTreeClassifier, show)
    print("tree score :", tree_score*100, "%")
    forest_score = generic_tree_score(X, y, matt, vect, RandomForestClassifier, show)
    print("forest score :", forest_score*100, "%")
