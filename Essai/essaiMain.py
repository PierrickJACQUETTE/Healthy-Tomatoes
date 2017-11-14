import essaiOperator as op
import BDD as bdd
import os, sys

op.BDDfromCSV(sys.argv[1], bdd.tableMovie);
#print(op.BDDSearchAll())
print(op.BDDSearchCategorie("title", "Avatar"))

