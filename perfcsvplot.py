#!/usr/bin/python

# Basic script to import CSV files exported with perfcall script and plotting them.    
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
import csv
import sys
import json

x = [],[]
y = []
x_array = []
y_array = []
cpu_array =[]

#Open the CSV:
data = sys.argv[1]
with open(data, 'rb') as csvfile:

	ylabel = 'Energy (Joules)'
	unit = 'Joules'
	
	query = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
	
	for row in range(23):
		if row == 1:
			date = next(query)
		elif row == 2:
			uname = next(query)
		elif row == 6:
			title = next(query)
		elif row == 11:
			cores = next(query)
		elif row == 13:
			time_interval = next(query)
		elif row == 17:
			number_cores = next(query)
		else:
			next(query)

	#Cores array to int array:
	cores = map(int, cores)
	#Number of cores from list to int:
	number_cores = map(int, number_cores)

	#Arrays global time and power:
	for row in query:
		x = row[0]
		x = float(x)
		x_array.append(x) #column 0 to array
		cpu = row[1]
		cpu_array.append(cpu) #column 0 to array
		y = row[2]
		y = float(y)
		y_array.append(y) #column 2 to array

#Operating with the CSV arrays parsed:
energy_core_ord_array = []
time_ord_array = []
#Dividing array into energy and time per core:
for i in range(number_cores[0]):
	e =  0 + i
	for j in range(len(x_array)/(int(number_cores[0]))):
		time_ord = x_array[e]
		time_ord_array.append(time_ord)
		energy_core_ord = y_array[e]
		energy_core_ord_array.append(energy_core_ord)
		e = e + int(number_cores[0])

#Getting real time lenght and energy array per core:
final_time_ord_array = []
for i in range(len(x_array)/(int(number_cores[0]))):
	final_time_ord = time_ord_array[i]
	final_time_ord_array.append(final_time_ord)
final_energy_core_ord_array = []
a = 0
for j in range(number_cores[0]):
	for i in range(len(x_array)/(int(number_cores[0]))):
		final_energy_core_ord = energy_core_ord_array[a + i]
		final_energy_core_ord_array.append(final_energy_core_ord)
	globals()['core%s' % j] = final_energy_core_ord_array
	final_energy_core_ord_array = []
	a = a + 12

#TEST: Printing Time and CPU arrays
print ''
print 'Final time'
print final_time_ord_array
print ''
for j in range(number_cores[0]):
	print cpu_array[j]
	print globals()['core%s' % j]
print ''

#Calculating time interval and defining title:
time_interval = float(time_interval[0])/1000
title = str(title)

#Calculating sum of energy array per core:
for j in range(number_cores[0]):
	total_joules = sum(globals()['core%s' % j])
	print "Total counts for: " + cpu_array[j] + " : %.2f" %total_joules +" "+ unit 
	total_time = len(final_time_ord_array)
	total_watt = total_joules / (total_time * time_interval)
	print "Total Power for: " + cpu_array[j] + " : %.2f Watts" %total_watt
	globals()['joules_cpu%s' % j] = total_joules
	globals()['watt_cpu%s' % j] = total_watt

#Defining plot with multiple cores:
for i in range(number_cores[0]):
	plt.plot(final_time_ord_array, globals()['core%s' % i], '-', linewidth=2)
'''
#Plot total energy per core:
indent = 0
for i in range(number_cores[0]):
	plt.figtext(0+indent, 0.02, cpu_array[i] + ": " + "%.2f" %globals()['watt_cpu%s' % i] +" Watts - "+"%.2f" %globals()['joules_cpu%s' % i] +" "+ unit)
	indent = indent + 0.2
'''
#Annotating each plot line to core:
indent = 0
for i in range(number_cores[0]):
	plt.annotate(cpu_array[i], xy=(final_time_ord_array[0], globals()['core%s' % i][0]), xytext=(final_time_ord_array[0],globals()['core%s' % i][0]+indent))
	indent = indent + 0.15

indent = 0
bbox_args = dict(boxstyle="round", fc="0.8")
for i in range(number_cores[0]):
	plt.text(final_time_ord_array[len(final_time_ord_array)-1],0.5+indent, cpu_array[i] + ": " + "%.2f" %globals()['watt_cpu%s' % i] +" Watts - "+"%.2f" %globals()['joules_cpu%s' % i] +" "+ unit, bbox=bbox_args)
	indent = indent + 0.5

#Configure axes:
plt.title(title)
plt.xlabel("Time (s)")
plt.ylabel(ylabel)
	
#Print plot:
plt.show()
print ''
print "Plot finished."

#--------------------------------------
#JSON export:
def json_dict(time,power, description):

	js_dict = dict(zip(
		["$schema",
		 "1title",
		 "2description",
		 "3date",
		 "4cpu",
		 "5time",
		 "6power"],
		["http://json-schema.org/draft-04/schema#",
		 "Perfcall and Perfcsvplot JSON export",
		  description,
		  date,
		  uname,
		  time,
		  power]
	))
	return js_dict

j_dict = json_dict(final_time_ord_array, y_array, title)

with open('output.json', 'w') as outfile:
	outfile.write(json.dumps(j_dict, indent=4, sort_keys=True, separators=(',', ': ')))

print ''
print "JSON export finished."
print "Bye!"

#Exit script
sys.exit()
