# Healthy-Tomatoes
Projet DataMining

https://www.kaggle.com/tmdb/tmdb-movie-metadata

-> Calculer la moyenne, l'écart type et la mediane de l'ensemble de train des vote_average
	enfin de fixer la note limite entre success et echec (modifier la note mediane de 5 pour l'instant)

-> Definir les poids sur les colonnes

-> Tfdif sur TRAIN avec des poids sur les colonnes, recuperer le dict pour pouvoir l'appliquer quand on teste avec l'ensemble de TEST

-> Regarder pour mot de chaque champs du film f appartenant a l'ensemble TEST
	quelque est la valeur du champ SUCCESS du film ayant l'idf le plus proche pour ce mot => soit 0 ou 1 
	faire la somme des valeurs de chaque mot (avec les poids) => ca donne un nombre
	donc on sait si cela est un succés si plus de 1 que de 0

-> Validation croisee

-> Chercher une librairie de Test unitaire

-> Faire un exemple sur la librairie de Test
