import numpy
import matplotlib.pyplot as plt

#put your log file here
filename = "log.lammps"

#I write thermo data with the following:
#thermo_style custom time temp epair etotal press c_PEnergyM c_KEnergyM
#c_PEnergyM c_KEnergyM are potential and kinetic energy for a group I defined

#thermo data in lines between these: update as appropriate
startstring = "Time Temp" #partial header line for data in log file
endstring = "Loop time" #line start following thermo data output in log file

#new file for writing data of interest (will overwrite existing)
datafile=open("simdata.out","w") 

#known headers/columns from log file / thermo_style: update as appropriate
datafile.write("Time Temp E_pair TotEng Press PEnergyM KEnergyM\n")

#logical for copying log file lines to data file: initialize as 0: not writing
writedata = 0

#data of interest appears on own lines, each line formatted same
#open log file and proceed line by line
#order of if statements is important here
with open(filename) as log:
    for num, line in enumerate(log, 0):
        if endstring in line: #reached end of data; stop writing
            writedata = 0
        if writedata == 1: #if we are in data, write the data line to the data file
            datafile.write(line)
        if startstring in line: #if we see the header for data, switch to writing data (will take effect with next line)
            writedata = 1
datafile.close()           

#open datafile as read-only so we don't have anything bad happen            
datafile=open("simdata.out","r")      
UsableArray = numpy.loadtxt(datafile, skiprows=1) #ignore header row
rowtotal = len(UsableArray[:,0]) #number of elements per column (number of rows)
coltotal = len(UsableArray[0,:]) #number of elements per row (number of columns)

#make some data vectors from extracted array: particular to your thermo output
Time = UsableArray[:,0] #vector of times
PE = UsableArray[:,5] #potential energy compute as function of time
KE = UsableArray[:,6] #kinetic energy compute as function of time

#optional: generate a little plot from data
plt.plot(Time, (KE+PE), 'ro')
plt.axis([Time[0], Time[rowtotal-1], min(PE+KE), max(PE+KE)])
plt.xlabel('Time (fs)')
plt.ylabel('Total Energy (Kcal/mole)')
plt.show()