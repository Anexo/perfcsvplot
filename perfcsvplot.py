# Basic script to import CSv files exported from Perf tool and plotting them.    
#------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import csv #For working with CSV
import sys

#Select the file:
print "Select the file to open (with path and extension)?"
data = raw_input("> ")
#Select the title and ylabel:
print "Select the title of the plot"
title = raw_input("> ")
print "Select the Y label of the plot"
ylabel = raw_input("> ")

#Open the CSV:
with open(data, 'rb') as csvfile:
	query = csv.reader(csvfile, delimiter=',')
	for row in query:
		print ', '.join(row)

#Ejemplo con el seno: 
x = np.linspace(0, 10)
line, = plt.plot(x, np.sin(x), '-', linewidth=2)

#Print plot:
plt.title(title)
plt.xlabel('Time (s)')
plt.ylabel(ylabel)
plt.show()
print "Plot finished. Bye!"

#Exit script
sys.exit()
