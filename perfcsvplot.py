#!/usr/bin/python

#Basic script to import CSV files exported with perfcall script and plotting them.    
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
import sys
import json
import pandas as pd
import csv
import operator

#Getting data from header:
data = sys.argv[1]
with open(data, 'rt') as csvfile:
	unit = 'Joules'
	query = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
	for row in range(23):
		if row == 1:
			date = next(query)
		elif row == 2:
			uname = next(query)
		elif row == 6:
			title = next(query)
		elif row == 13:
			time_interval = next(query)
		elif row == 17:
			number_cores = next(query)
		else:
			next(query)

#Open the CSV:
csvfile = sys.argv[1]

#The data read by csv reader into data variable:
data = pd.read_csv(csvfile, header=None, skipinitialspace=True, skiprows=23, names=['time'], usecols=[0], delimiter=';')
#print data

#Formatting time array
times = list(pd.unique(data.time.ravel()))

#The data read by csv reader into data variable:
data = pd.read_csv(csvfile, header=None, skipinitialspace=True, skiprows=23, names=['cpu', 'energy','unit','event'], usecols=[1,2,3,4], delimiter=';', decimal=',')
#print data

#Group data by CPU
cpuList = data.groupby(['cpu'])

#CPU dict
cpuEnergy = {}

#Loop for indexing CPU and energy
for i in range(len(cpuList)):
    eachCPU = 'CPU' + str(i+1)
    cpuEnergy[eachCPU] = list(cpuList.get_group('CPU' + str(i+1))['energy'])

'''
#print CPU data
for k, v in cpuEnergy.items():
    print k, v
'''

#Calculating sum of energy array per core:
total_joules_array = []
total_watt_array = []
total_time = times[-1] - times[0]
for k, v in cpuEnergy.items():
	total_joules = sum(v)
	total_joules_array.append(total_joules)
	total_watt = total_joules/total_time
	total_watt_array.append(total_watt)

'''
print total_watt_array
print total_joules_array
'''

#Defining plot with multiple cores:
for k, v in cpuEnergy.items():
	plt.plot(times, v, '-', linewidth=2)

#Annotating each plot line to core:
indent = 0
for k, v in cpuEnergy.items():
	plt.annotate(k, xy=(times[0], v[0]), xytext=(times[0],v[0]+indent))
	indent = indent + 0.3

#Calculating time interval and defining title:
time_interval = float(time_interval[0])/1000

#Plot total energy per core:
indent = 0
bbox_args = dict(boxstyle="round", fc="0.8")
for k,v in cpuEnergy.items():
	total_joules = sum(v)
	total_watt  = total_joules / total_time
	plt.text(times[-1], 0.5+indent, k + ' ' + "%.2f" %total_watt + ' Watts - ' + "%.2f" %total_joules + ' Joules', bbox=bbox_args)
	indent = indent + 0.5

#Configure axes:
plt.title(title)
plt.xlabel('Time (s)')
plt.ylabel('Energy (Joules)')

#Print plot:
plt.show()
print ('')
print ('Plot finished.')

#JSON export:
def json_dict(time,power, description):

	js_dict = dict(zip(
		["1title",
		 "2description",
		 "3date",
		 "4cpu",
		 "5time",
		 "Cores"],
		["Perfcall and Perfcsvplot JSON export",
		  str(description),
		  str(date),
		  str(uname),
		  time,
		  cpuEnergy]
	))
	return js_dict

j_dict = json_dict(times, cpuList, title)

with open('output.json', 'w') as outfile:
	outfile.write(json.dumps(j_dict, indent=4, sort_keys=True, separators=(',', ': ')))

print ('')
print ("JSON export finished.")
print ("Bye!")