from elasticsearch import helpers, Elasticsearch
import BDD as bdd
import csv


medianeVoteAverage = 6.2

##permet de stocker dans elasticsearch les donnees dans fichiers
#@param csv_filenameMovie chemin du fichier des films
#@param csv_filenameCredit chemin du fichier des credits
#@param tableTrain name table d'entrainement
#@param tableTest name table de test
#@param numberSeparation nombre ou la separation a lieu entre les deux tables
def BDDfromCSV(csv_filenameMovie, csv_filenameCredit, tableTrain, tableTest, numberSeparation):
	es = bdd.BDD.get_instance();
	try :
		es.indices.delete(index=bdd.index)
	except :
		pass

	es.indices.create(index=bdd.index)
	print("now indexing...")

	with open(csv_filenameMovie, errors='replace') as csvfileMovie, open(csv_filenameCredit) as csvfileCredit :
		readerMovie = csv.DictReader(csvfileMovie)
		readerCredit = csv.DictReader(csvfileCredit)
		i = 2
		for row, row2 in zip(readerMovie, readerCredit) :
			try :
				vote = float(row['vote_average'])
				if(vote > medianeVoteAverage and vote <= 10):
					row['SUCCESS'] = 1
				elif(vote <= medianeVoteAverage and vote >= 0):
					row['SUCCESS'] = 0
				else:
					newVote = vote%10
					row['vote_average'] = newVote
					row['SUCCESS'] = newVote
				rowTotal = {**row, **row2}
				if(i<numberSeparation):
					es.index(index=bdd.index, doc_type=tableTrain, body=rowTotal)
				else:
					es.index(index=bdd.index, doc_type=tableTest, body=rowTotal)
			except :
				print("Error row : ", i)
				pass
			i = i+1
			if(i%250 == 0):
				print("Add rows : ", i)

##cherche dans la table, la requete et renvoi le resultat
#@param query requete a faire dnas la base
#@param table sur quel table effectue la requete
#@return resultat de la requete
def BDDSearch(query, table):
	es = bdd.BDD.get_instance();
	res = es.search(index=bdd.index, doc_type=table, body=query, size=4000)
	return res

##cherche dans la table train, tout les documents
#@return resultat de la requete
def BDDSearchAll():
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"]}
	#myquery={"query":{"match_all":{}}}
	return BDDSearch(myquery, bdd.tableMovieTrain);

##cherche dans la table train, tout les documents ayant tel key et value
#@param key le champs sur lequel faire une requete
#@param value la valeur du champs
#@return resultat de la requete
def BDDSearchCategorie(key, value):
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"], "query" : {"match" : {key : value}}}
	return BDDSearch(myquery, bdd.tableMovieTrain);

##cherche dans la table test, tout les documents
#@return resultat de la requete
def BDDSearchAllTest():
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"]}
	#myquery={"query":{"match_all":{}}}
	return BDDSearch(myquery, bdd.tableMovieTest);

##cherche dans la table test, tout les documents ayant tel key et value
#@param key le champs sur lequel faire une requete
#@param value la valeur du champs
#@return resultat de la requete
def BDDSearchCategorieTest(key, value):
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"], "query" : {"match" : {key : value}}}
	return BDDSearch(myquery, bdd.tableMovieTest);
