import csv
import numpy as np

res = dm
csvfile = "dmdm.cvs"
 
np.savetxt(csvfile, res, delimiter=",")