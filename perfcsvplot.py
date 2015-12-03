#!/usr/bin/python

# Basic script to import CSV files exported from Perf tool and plotting them.    
#------------------------------------------------------------------------------

#Copyright (C) 2015 by Tomas Lopez-Fragoso Rumeu <https://github.com/Anexo>
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>
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
#Select the title, ylabel, time interval and unit:
print "Select the title of the plot"
title = raw_input("> ")
print "Select the Y label of the plot"
ylabel = raw_input("> ")
print "Time interval (For 500ms enter 0.5)?"
time_interval = float(raw_input("> "))
print "Unit measured?"
unit = raw_input("> ")

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

#Calculating sum of x_array:
total_y = sum(y_array)
print "Total counts: %.2f" %total_y +" "+ unit 
#Energy in Watt if nedeed:
if unit.lower() == "joules":
	total_time = len(x_array)
	total_watt = total_y / (total_time * time_interval)
	print "Total Power: %.2f Watts" %total_watt

#Defining plot:
line, = plt.plot(x_array, y_array, '-', linewidth=2)

#Configure axes:
plt.title(title)
plt.xlabel("Time (s)")
plt.ylabel(ylabel)

#Plot total energy:
if unit.lower() == "joules":
	plt.figtext(0.6, 0.02, "%.2f" %total_watt +" Watts - "+"%.2f" %total_y +" "+ unit)
else:
	plt.figtext(0.6, 0.02, "%.2f" %total_x +" "+ unit)
	
#Print plot:
plt.show()
print "Plot finished. Bye!"

#Exit script
sys.exit()
