from elasticsearch import helpers, Elasticsearch

index = "fouille"
tableMovieTrain = "TrainMovie"
tableMovieTest = "TestMovie"
tableCreditTrain = "TrainCredit"
tableCreditTest = "TestCredit"

#permet d'avoir une seule instance de la base
class BDD:
	INSTANCE = None

	@classmethod
	def get_instance(cls):
		if cls.INSTANCE is None:
			cls.INSTANCE = Elasticsearch([{'host': 'localhost', 'port': 9200}]);
		return cls.INSTANCE
