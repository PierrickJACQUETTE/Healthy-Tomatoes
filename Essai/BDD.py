from elasticsearch import helpers, Elasticsearch

index = "fouille"
tableMovie = "movie"
tableCredit = "credit"

class BDD:
	INSTANCE = None

	@classmethod
	def get_instance(cls):
		if cls.INSTANCE is None:
			cls.INSTANCE = Elasticsearch([{'host': 'localhost', 'port': 9201}]);
		return cls.INSTANCE
