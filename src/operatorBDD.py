from elasticsearch import helpers, Elasticsearch
import BDD as bdd
import csv


medianeVoteAverage = 6.2

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
				l = []
				# vote = float(row['vote_average'])
				# if(vote > medianeVoteAverage and vote <= 10):
				# 	row['SUCCESS'] = 1
				# elif(vote <= medianeVoteAverage and vote >= 0):
				# 	row['SUCCESS'] = 0
				# else:
				# 	newVote = vote%10
				# 	row['vote_average'] = newVote
				# 	row['SUCCESS'] = newVote
				# rowTotal = {**row, **row2}
				# if(i<numberSeparation):
				# 	es.index(index=bdd.index, doc_type=tableTrain, body=rowTotal)
				# else:
				# 	es.index(index=bdd.index, doc_type=tableTest, body=rowTotal)
			except :
				print("Error row : ", i)
				pass
			i = i+1
			if(i%250 == 0):
				print("Add rows : ", i)

def BDDSearch(query, table):
	es = bdd.BDD.get_instance();
	res = es.search(index=bdd.index, doc_type=table, body=query, size=4000)
	return res

def BDDSearchAll():
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"]}
	#myquery={"query":{"match_all":{}}}
	return BDDSearch(myquery, bdd.tableMovieTrain);

def BDDSearchCategorie(key, value):
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"], "query" : {"match" : {key : value}}}
	return BDDSearch(myquery, bdd.tableMovieTrain);

def BDDSearchAllTest():
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"]}
	#myquery={"query":{"match_all":{}}}
	return BDDSearch(myquery, bdd.tableMovieTest);

def BDDSearchCategorieTest(key, value):
	myquery={"_source": ["SUCCESS", "title", "vote_average", "vote_count", "budget", "genres", "production_companies", "keywords", "cast", "crew"], "query" : {"match" : {key : value}}}
	return BDDSearch(myquery, bdd.tableMovieTest);
