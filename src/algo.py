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
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#permet de savoir si c'est un echec ou succes
def naiveBayes(lt, dic, mat, vec) :
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
        # print(i, res, per)
        if(i == 1 and res >= 0) :
            true += 1
        elif (i == 0 and res < 0) :
            true += 1
        else :
            fail += 1

    print("OK : ", true)
    print("KO : ", fail)

#permet de savoir le meilleur k possible
def find_best_k_for_kneighbors(X, y, n_splits=5):
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    skf = StratifiedKFold(n_splits=n_splits)

    best_k = 1
    best_score = 0

    for k in range(1, 100, 2):
        score_sum = 0.0

        for train_idx, test_idx in skf.split(X_train, y_train):
            X_subtrain, X_subtest = X[train_idx], X[test_idx]
            y_subtrain, y_subtest = y[train_idx], y[test_idx]

            model = KNeighborsClassifier(k, n_jobs=-1).fit(X_subtrain, y_subtrain)
            score = model.score(X_subtest, y_subtest)

            score_sum += score

        score_sum /= n_splits
        if score_sum > best_score:
            best_score = score_sum
            best_k = k

    return best_k

#permet de savoir si c'est un echec ou succes
def accuraccy_test(X, y, tfidf, k=77):
    a = op.BDDSearchAllTest();
    s = to.getSize(a)
    print(s)
    d = []
    d.append(a)
    l = to.createList(d, s)
    mat, vec, tfidfTest = to.transform(l, to.getDict(tfidf))
    knn = KNeighborsClassifier(k, n_jobs=-1)
    knn.fit(X, y)
    score = knn.score(mat, vec)
    return score*100

#permet de savoir les meilleurs parametres
def generic_tree(X, y, cls):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits)
    best_min_samples_split = 2
    best_max_depth = None
    best_score = 0
    max_depths = list(range(1, 20+1))
    max_depths.append(100)
    max_depths.append(None)
    for min_samples_split in range(2, 20+1):
        for max_depth in max_depths:
            score_sum = 0.0
            for train_idx, test_idx in skf.split(X_train, y_train):
                X_sub_train, X_sub_test = X[train_idx], X[test_idx]
                y_sub_train, y_sub_test = y[train_idx], y[test_idx]
                model = cls(min_samples_split=min_samples_split, max_depth=max_depth)
                model.fit(X_sub_train, y_sub_train)
                score = model.score(X_sub_test, y_sub_test)
                score_sum += score
                score_average = score_sum / n_splits
            if score_average > best_score:
                best_score = score_average
                best_min_samples_split = min_samples_split
                best_max_depth = max_depth
    return best_min_samples_split, best_max_depth

#permet de savoir si c'est un echec ou succes
def generic_tree_score(X, y, tfidf, cls):
    a = op.BDDSearchAllTest();
    s = to.getSize(a)
    d = []
    d.append(a)
    l = to.createList(d, s)
    mat, vec, tfidfTest = to.transform(l, to.getDict(tfidf))
    best_min, best_max = generic_tree(X, y, cls)
    m = cls(min_samples_split=best_min, max_depth=best_max)
    m.fit(X, y)
    score = m.score(mat, vec)
    return score

#permet de lancer pour les deux arbres
def algoTree(X, y, tfidf):
    tree_score = generic_tree_score(X, y, tfidf, DecisionTreeClassifier)
    print("tree score :", tree_score*100, "%")
    forest_score = generic_tree_score(X, y, tfidf, RandomForestClassifier)
    print("forest score :", forest_score*100, "%")
