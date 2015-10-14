# Basic script to import CSv files exported from Perf tool and plotting them.    
#------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy
import csv #For working with CSV
import sys

#Open the CSV:
with open('/home/tomas/Escritorio/Doctorado/Programas/python/A1000.csv', 'rb') as csvfile:
	query = csv.reader(csvfile, delimiter=',')
	for row in query:
		print ', '.join(row)

'''
print "Plot:" 
plt.show()

print "Done!"
sys.exit()
'''
