# -------------------------------------------------------------------------- #
# 		ABOUT 
# -------------------------------------------------------------------------- #
# Created: May 19th 2016
# Author:  Stephanie Lauber
# Last updated: May 25th 2016 by Stephanie Lauber

# This script is used to replace theoretical values contained in .gtr file 
# with the following experimental values:
#	- parent binding energy
# 	- daughter binding energy
#	- parent excitation states
# 	- daugther excitation states
#	- transition strengths

# It assumes the input file is formatted in the following way:
# 	- Col1  Name of transition .gtr file
#	- Col2  Number of parent state to replace 
# 	- Col3  Number of daugther state to replace
# 	- Col4  J associated with each daugther state to replace
# 	- Col5  T associated with each daughter state to replace
#	- Col6  Parent experimental excitation energy
#	- Col7  Daugther experimental excitation energy
#	- Col8  Parent experimental binding energy
#	- Col9  Daugther experimental binding energy
# 	- Col10 Experimental transition strength

# The script reads the experimental information from the data file into an 
# astropy table (will be updated to a more general function). The number of
# replacements necessary for each nuclide is determined by matching the name
# of the transition in Column 1. For each nuclide transition, the associated
# number of the parent and daughter state are used for the replacement. 

# The function replaceValues uses this numbers to search for the associated
# states and replaces the theoretical values with experimental data points and
# flags as "T" for from exp? 

# A new file is created with the extention _expt.gtr and the original file
# is not modified. The .gtr file is then converted to a .gtb file.

# Required in the working directory:
#	- .gtr files to be replaced
#	- gtconvertible.v2.f90 as gtconvertible
# 	- file containing experimental data for replacement 

# -------------------------------------------------------------------------- #
# 		IMPORT FUNCTIONS
# -------------------------------------------------------------------------- #
import numpy as np 
import os
import fileinput as fi 
import linecache as lc 

# -------------------------------------------------------------------------- #
# These were NOT present on SunWuKong --
# I will modify the script to include a more general python function for 
# obtaining the information from the input file containing exp values.
# -------------------------------------------------------------------------- #
from StringIO import StringIO
from astropy.table import Table 

# -------------------------------------------------------------------------- #
def replaceValues( file_name, Pnum, Dnum, Dex, Pex, Pbe, Dbe, Bgt, repNum ):
# -------------------------------------------------------------------------- #
# Input:	file_name	
#			Pnum		Parent number
#			Dnum		Daughter number
#			Dex			Daughter excitation energy
#			Pex			Parent excitation energy
#			Pbe			Parent binding energy for g.s.
#			Dbe			Daughter binding energy for g.s.
#			Bgt 		Experimental B(GT) values
#			repNum		Number of replacement values

	out_name   = str( file_name ) + "_expt.gtr"
	input_name = str( file_name ) + "_input.dat"
	file_gtb   = str( file_name ) + "_expt"
	file_gtr   = str( file_name ) + "_expt"
	file_name  = str( file_name ) + ".gtr"
	file_data  = fi.input( file_name )
	file_out   = open( out_name, "w" )
	rep_lines  = []

	# Replace necessary data points
	for line in file_data:
		# Find the line to replace parent BE
		# Find the line to replace parent excitation
		if line.find('! parent Z, N, E g.s.') != -1:
			rep_lines.append( fi.lineno() + 1 )
			rep_lines.append( fi.lineno() + 5 )
		# Find the line to replace daughter BE
		# Find the line(s) to replace daughter excitation(s)
		elif line.find('! daughter Z, N, E g.s.') != -1:
			rep_lines.append( fi.lineno() + 1 )
			rep_lines.append( fi.lineno() + 4 ) 
		# Find line(s) to replace B(GT) values
		elif line.find('  ! parent, daughter, B-value, from expt? ') != -1:
			rep_lines.append( fi.lineno() + 1 )

	
	# Add last point to rep_lines for stop
	rep_lines.append(-99)

	j = 0	# Counter for number of starting replacement lines
	k = 0 	# Counter for number of experimental replacements
	m = 0	# Counter for daugther excitations 
	n = 0	# Counter for B(GT) replacements 

	# Inport data from theoretical .gtr files
	file_data = fi.input( file_name )

	while k < repNum:
		for line in file_data:
			# End of replacement lines has been reached
			if rep_lines[j] == -99:
				print "All lines have been replaced \n"
				break

			# Replace parent ground state energy
			elif fi.lineno() == rep_lines[0] - 1:
				file_out.write(line)
				parent_data = lc.getline( file_name, fi.lineno()+1 ).split()
				parent_Z    = int(parent_data[0])
				parent_N    = int(parent_data[1])
				file_out.write('%4i%4i%12.5f \n' % (parent_Z, parent_N, Pbe))
			
				# Increment j and move to next line in file
				j = j + 1
				line = file_data.next()

			# Replace daughter ground state energy
			elif fi.lineno() == rep_lines[2] - 1:
				file_out.write(line)
				daughter_data = lc.getline( file_name, fi.lineno()+1 ).split()
				daugther_Z    = int(daughter_data[0])
				daughter_N    = int(daughter_data[1])
				file_out.write('%4i%4i%12.5f \n' % (daugther_Z, daughter_N, Dbe))
			
				# Increment j and move to next line in file
				j = j + 1
				line = file_data.next()

			# Start of parent excitation energies
			elif fi.lineno() == rep_lines[1] - 1:
				file_out.write(line)
				parent_exct = lc.getline( file_name, fi.lineno()+1 ).split()
				if int(parent_exct[0]) == Pnum[0]:
					file_out.write('%4i%5.1f%5.1f%12.4f  %1s \n' % ( int(parent_exct[0]), float(parent_exct[1]),
						float(parent_exct[2]), Pex[0], 'T' ) )
					line = file_data.next()
				else:
					file_out.write(line)

			# Start of daugther excitation energies
			elif fi.lineno() == rep_lines[3] - 1:
				file_out.write(line)
				while m < repNum:
					# Match theoretical and experimental daugther state number
					daughter_exct = lc.getline( file_name, fi.lineno()+1 ).split()
					if int(daughter_exct[0]) == Dnum[m]:
						file_out.write('%4i%5.1f%5.1f%12.4f  %1s \n' % ( int(daughter_exct[0]), float(daughter_exct[1]),
							float(daughter_exct[2]), Dex[m], 'T') )
						m = m + 1
						line = file_data.next()
					else:	
						line = file_data.next()	
						file_out.write(line)			

			# Start of B(GT) values
			elif fi.lineno() == rep_lines[4] - 1:
				file_out.write(line)
				while n < repNum:
					BGT_data = lc.getline( file_name, fi.lineno()+1 ).split()
					if int(BGT_data[0]) == Pnum[0] and int(BGT_data[1]) == Dnum[n]:
						file_out.write('%5i%5i%12.4f  %1s \n' % ( int(BGT_data[0]), int(BGT_data[1]), Bgt[n], 'T') )
						n = n + 1
						line = file_data.next()
					else:
						line = file_data.next()
						file_out.write(line)

			# Copy normal line to new file
			else:
				file_out.write(line)
				k = k + 1

	file_out.close()

	# Input file for convertion code 
	input_file = open( input_name, "w" )
	input_file.write('3\n')
	input_file.write('%s\n' % file_gtr )
	input_file.write('%s\n' % file_gtb )
	input_file.close()

	# Convert experimental readible file to binary
	# Assumes convertion code is in working directory 
	cmd1 = "./gtconvertible < %s " % input_name 
	cmd2 = "rm %s " % input_name
	os.system( cmd1 )
	os.system( cmd2 )

	return 

# -------------------------------------------------------------------------- #
#				MAIN PROGRAM
# -------------------------------------------------------------------------- #

print ('# ................................................................ #')
print (' This program takes a file containing experimental data values for  ')
print (' parent and daugther ground state energies (binding energies),      ')
print (' excitation energies and matches them to theoretical values based on')
print (' the parent and daughter state number from Bigstick.                ')
print ('')
print (' The .gtr files provided will be coped to new _expt.gtr files with  ')
print (' the replaced experimental data points in the same directory.       ')
print ('')

# File containing experimental data
file_name = raw_input(' Enter file name and extension containing experimental values: ')

# Make sure file is in working directory 
check_for = file_name 
while not os.path.exists( check_for ):
	print ('')
	print (' !!! INCORRECT input file name name !!! ')
	file_name = raw_input(' Enter file name and extension containing experimental values: ')
	check_for = file_name
print ('')

# Import experimental data from given file
data = Table.read( str(file_name), format='ascii')
data.rename_column('col1', 'Names')
data.rename_column('col2', 'P Num')
data.rename_column('col3', 'D Num')
data.rename_column('col4', 'J')
data.rename_column('col5', 'T')
data.rename_column('col6', 'D Ex')
data.rename_column('col7', 'P Ex')
data.rename_column('col8', 'P BE')
data.rename_column('col9', 'D BE')
data.rename_column('col10', 'Bgt')

# Determine number of replacements to be performed
num_rows = data['Names'].shape
# Counter for nuclide to perform replacement
i = 0

while i < num_rows[0]:
	# Number of replacements counter
	repNum = 1

	# Determine number of replacements for a given nuclide
	for j in range(i,num_rows[0]-1):
		# If same nuclide
		if (data['Names'][j] == data['Names'][j+1]):
			repNum = repNum + 1
		# Not same nuclide
		else: 
			break

	# For each nuclide, replace with experimental values
	print "Replacing %i experimental value(s) for %s\n" % ( repNum, data['Names'][i] )
	replaceValues(data['Names'][i], data['P Num'][i:i+repNum], data['D Num'][i:i+repNum], 
		data['D Ex'][i:i+repNum], data['P Ex'][i:i+repNum], data['P BE'][i], data['D BE'][i],data['Bgt'][i:i+repNum], repNum)

	i = i + repNum

print ('')
print ('All values have been replaced.')
print ('END OF PROGRAM')
print ('# ................................................................ #\n\n')
