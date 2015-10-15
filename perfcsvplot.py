# Basic script to import CSv files exported from Perf tool and plotting them.    
#------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy
import csv #For working with CSV
import sys

#Select the file:
print "Select the file to open (with path and extension)?"
data = raw_input("> ")

#Open the CSV:
with open(data, 'rb') as csvfile:
	query = csv.reader(csvfile, delimiter=',')
	for row in query:
		print ', '.join(row)

'''
print "Plot:" 
plt.show()

print "Done!"
sys.exit()
'''
