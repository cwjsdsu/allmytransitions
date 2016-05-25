import os

# ----------------------------------------------------------------------- #
def createInputOpt1( nuclideName, aValue, decayName ):
# ----------------------------------------------------------------------- #
# Generates temporary input files for runing gtconvertible.v2.f90 for a 
# given nuclide and removes input file after completing. 

	file_name   = str( nuclideName ) + str( aValue ) + 'usdb' + str( decayName ) + '.dat'
	input_name  = str( nuclideName ) + str( aValue ) + 'usdb' + str( decayName )
	output_name = str( nuclideName ) + str( aValue )          + str( decayName )
	input_file  = open( file_name, "w" )

	input_file.write('0\n')
	input_file.write('%s\n' % input_name  )
	input_file.write('%s\n' % output_name )
	input_file.write('%s\n' % output_name )

	input_file.close()

	cmd1 = "gtcv2.x < %s " % file_name
	cmd2 = "rm %s" % file_name

	os.system( cmd1 )
	os.system( cmd2 )

	return

# ----------------------------------------------------------------------- #
# MAIN PROGRAM
# ----------------------------------------------------------------------- #

print('')
nuc_num = int(input(' \t Enter number of nuclides to convert: '))
# Total number of different nuclides 

nuclide_name = []	
nuclide_A    = []
decay_name   = []	# Bplus or Bminus

for i in range( nuc_num ):
	print('')
	print('Nuclide number %i of %i' % ( i+1, nuc_num ) )
	nuc_name = ( raw_input('\t Name of nuclide:    '))
	num_iso  =   int(input('\t Number of isotopes: '))
	dec_name = ( raw_input('\t Type of decay:      '))
	aStart   =   int(input('\t Starting A value:   '))

	# Populates list for name, A and decay type
	for j in range( num_iso ):
		nuclide_name.append( nuc_name )
		nuclide_A.append( aStart + j )
		decay_name.append( dec_name )

for i in range( len(nuclide_name) ):
	createInputOpt1( nuclide_name[i], nuclide_A[i], decay_name[i] )
