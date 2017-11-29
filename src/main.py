import operatorBDD as op
import BDD as bdd
import os, sys

#op.BDDfromCSV(sys.argv[1], bdd.tableMovieTrain, bdd.tableMovieTest, 3900)
print(op.BDDSearchAll())
#print(op.BDDSearchCategorie("title", "Avatar"))
#print(op.BDDSearchCategorie("genres", "Action"))
#print(op.BDDSearchCategorie("vote_average", "7.2"))
