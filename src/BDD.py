from elasticsearch import helpers, Elasticsearch

index = "fouille"
tableMovieTrain = "TrainMovie"
tableMovieTest = "TestMovie"
tableCreditTrain = "TrainCredit"
tableCreditTest = "TestCredit"

class BDD:
	INSTANCE = None

	@classmethod
	def get_instance(cls):
		if cls.INSTANCE is None:
			cls.INSTANCE = Elasticsearch([{'host': 'localhost', 'port': 9200}]);
		return cls.INSTANCE
