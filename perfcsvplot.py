# Basic script to import CSV files exported from Perf tool and plotting them.    
#------------------------------------------------------------------------------

#**"THE COFFEEWARE LICENSE" (Revision 2):**
#------------------------------------------
#Anexo[1] wrote this code. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a coffee in return. 
#
#Also, you might consider following me on [social network][2] for any comments and/or questions you might have and if you'd like you can send me a donation at any time to support my work, ask me how!
#
#  [1]: http:tomaslopezfragosorumeu.com
#  [2]: https://github.com/Anexo
#------------------------------------------

import matplotlib.pyplot as plt
import csv #For working with CSV
import sys

x = []
y = []
x_array = []
y_array = []

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
	#Check if header present:
	has_header = csv.Sniffer().has_header(csvfile.read(1024))
	csvfile.seek (0) #return to top
	
	query = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
	
	if has_header:
		next(query) #Skip header
		next(query)	#Skip blank row
	for row in query:
		x = row[0]
		x = float(x)
		x_array.append(x) #column 0 to array

		y = row[1]
		y = float(y)
		y_array.append(y) #column 1 to array

#Defining plot:
line, = plt.plot(x_array, y_array, '-', linewidth=2)

#Print plot:
plt.title(title)
plt.xlabel('Time (s)')
plt.ylabel(ylabel)
plt.show()
print "Plot finished. Bye!"

#Exit script
sys.exit()
