import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def spin_flip(d, J, M, T, L, nlattice):
	# Choose a lattice point at random
	dim = [0]*d 
	for i in range(d):
		dim[i] = np.random.randint(0,L)
	x = dim[0]
	y = dim[1]
	
	# Calculate dE
	dE = ( 2*J*nlattice[y][x]*(nlattice[(y+1)%L][x%L]
				+nlattice[(y-1)%L][x%L]
				+nlattice[y%L][(x+1)%L]
				+nlattice[y%L][(x-1)%L]) )
	# Calculate acceptance and attempt flip
	R = math.exp(-dE/T)
	if R >= 1:
		lattice[y][x] *= -1
		M += 2.*nlattice[y][x]/(L*L)
	
	elif R > np.random.random():
		lattice[y][x] *= -1
		M += 2.*nlattice[y][x]/(L*L)
	
	return M, nlattice

## Creates a block and its corresponding block sizes and no. and counters
def create_blocks():
	Z = 10 # Size of blocks
	Nb = 100 # No. of blocks
	block = 0 # block term counter
	zcounter = -1 # term inside the block counter
	blocks = [[0 for val in range(Z)] for bloc in range(Nb)]
	return blocks, Z, Nb, block, zcounter
	
	
## Updates block array ##
def update_blocks(M, Mblocks, Z, Nb, zcounter, block):
	zcounter += 1

	Mblocks[block][zcounter] = M
	
	if zcounter == Z-1:
		block += 1
		zcounter = -1
		
	if block == Nb: # tests if array of blocks are full
		Mblocks, block, Z = move_values(Mblocks, block, Z, Nb)
				
	return Mblocks, zcounter, block, Z

## Concatenates pairs of block to create space for new measurements ##
def move_values(Mblocks, block, Z, Nb):
	Z *= 2
	new_Mblocks = [[0 for i in range(Z)] for j in range(Nb)]
	for n in range(Nb//2):
		new_Mblocks[n] = Mblocks[2*n] + Mblocks[2*n+1]
	block = 50 
	return new_Mblocks, block, Z

## Calculated the error for a given block array
def stdev(Mblocks, Nb, Z):
	blockarray = []
	for i in range(len(Mblocks)):
		blockarray.append(sum(Mblocks[i])/Z)
	blockarray = [x for x in blockarray if x != 0]
	avgblock = sum(blockarray)/len(blockarray)
	block_minus_average = []
	for i in range(len(blockarray)):
		a = blockarray[i] - avgblock
		block_minus_average.append(a*a)
	std = (1./Nb) * math.sqrt(sum(block_minus_average)) 
	return std

"""Start of code, initialize variables"""

d = 2 # Lattice Dimensions
Llist = [4,8,16,32] # List of lattice side lengths
J = 1 # Energy/Temperature ratio
N = 2000000 # Number of iterations
M = 0.
# The following are lists which will lists of measurements of observables
# and their errors of varies system sizes
M_plots = []
stdM_plots = []
binder_plots = []
stdbinder_plots = []
chi_plots = []
stdchi_plots = []
for L in Llist: 
	T_list = [] # List containing the temperatures
	avgM_list = [] # List containing the average magnetisations
	avgstd_list = [] # List containing the average standard deviations
	binder_list = [] # binder ratios
	stdbinder_list = [] # binder ratios error
	chi_list = [] # Magnetic susceptibility
	stdchi_list = [] # susceptibility error
	print(L , ' done')
	# for subsequent plotting of the spin glass
	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 12))
	
	
	### INITIALIZING LATTICE AND ARRAY OF BLOCKS ###
	# Make a LxL array all zeros
	inlattice = [[0 for x in range(L)] for y in range(L)]
	for y in range(L): # Initialize the spin configuration lattice
		for x in range(L):
			inlattice[y][x] = int(np.random.randint(0,2) * 2 - 1)

	for T in np.arange(1.5, 4.5, 0.1):
		dE = 0. # change in energy
		R = 0. # acceptance ratio
		M = 0. # Total magnetisation
		Mlist = [] # List of magnetisation values
		M2list = [] # List of magnetisation squared values

		lattice = inlattice
		
		for y in range(L): # Initialize the spin configuration lattice
			for x in range(L):
				M += float(lattice[y][x])/(L*L)
			
		# Mblocks contains all the magnetisation measurements stored in a 2d
		# array, where each row contains a block, and the
		# values in the row are the measurements
		Mblocks, Z, Nb, block, zcounter = create_blocks()
		# M2blocks will contain the square of the magnetisations,
		# it has its own set of counters and block sizes
		M2blocks, Z2, Nb2, block2, zcounter2 = create_blocks()

		### RUN ALGORITHM FOR N ITERATIONS ###
		for n in range(N):
			#print M
			M , lattice = spin_flip(d, J, M, T, L, lattice)
			Mlist.append(abs(M))
			M2 = M*M
			M2list.append(M2)
			
			Mblocks, zcounter, block, Z = update_blocks(M, Mblocks,
			Z, Nb, zcounter, block)
			M2blocks, zcounter2, block2, Z2 = update_blocks(M2, M2blocks,
			Z2, Nb2, zcounter2, block2)
		
		# Plots lattice configuration
		if L == 32:
			fig.clf()
			ax = fig.add_subplot(1, 1, 1)
			im_content = ax.imshow(lattice, cmap=cm.afmhot,
			interpolation='nearest')
			fig_name = 'B' + str(round(T,2)) + '.png'
			plt.savefig(fig_name, bbox_inches='tight')
			
		# magnetisations
		avgM = sum(Mlist)/len(Mlist)
		avgM2 = sum(M2list)/len(M2list)
		avgM3 = avgM*avgM
		avgstd = stdev(Mblocks, Nb, Z)
		stdM2 = stdev(M2blocks, Nb2, Z2)
		stdM3 = avgM3*2*(avgstd/avgM)
		
		# Binder ratios
		binder =  (avgM2) / (avgM3)
		stdbinder = binder*math.sqrt( (stdM2/avgM2)**2 + (stdM3/avgM3)**2 )
		
		# Susceptibility
		chi = (L*L) * (1./T) * (avgM2 - avgM3)
		stdchi = ((L*L)) * (1./T) * math.sqrt( stdM2**2 + stdM3**2 )
		
		# Create list of measurements
		T_list.append(T)
		avgM_list.append(avgM)
		avgstd_list.append(avgstd)
		binder_list.append(binder)
		stdbinder_list.append(stdbinder)
		chi_list.append(chi)
		stdchi_list.append(stdchi)
	
	# Creates list of lists of measurements
	M_plots.append(avgM_list)
	stdM_plots.append(avgstd_list)
	binder_plots.append(binder_list)
	stdbinder_plots.append(stdbinder_list)
	chi_plots.append(chi_list)
	stdchi_plots.append(stdchi_list)

# Removes the first element in each list of observables to fix the issue
# of thermalization at the start
for w in range(len(Llist)):
	M_plots[w].pop(0)
	stdM_plots[w].pop(0)
	binder_plots[w].pop(0)
	stdbinder_plots[w].pop(0)
	chi_plots[w].pop(0)
	stdchi_plots[w].pop(0)
T_list.pop(0)

### Plots ###
name = 'magnetisation'
name2 = 'Binder'
name3 = 'Susceptability'
plt.figure(name)
for s in range(len(Llist)):
	plt.errorbar(T_list, M_plots[s], stdM_plots[s], marker = 'x',
	capsize = 2, label = "System Size %s" %Llist[s])
	plt.legend(loc="best")
plt.xlabel('Temperature')
plt.ylabel('Average magnetisation')

plt.figure(name2)
for s in range(len(Llist)):
	plt.errorbar(T_list, binder_plots[s], stdbinder_plots[s], marker = 'x',
	capsize = 2, label = "System Size %s" %Llist[s])
	plt.legend(loc="best")
plt.xlabel('Temperature')
plt.ylabel('Binder Ratio')

plt.figure(name3)
for s in range(len(Llist)):
	plt.errorbar(T_list, chi_plots[s], stdchi_plots[s], marker = 'x',
	capsize = 2, label = "System Size %s" %Llist[s])
	plt.legend(loc="best")
plt.xlabel('Temperature')
plt.ylabel('Magnetic Susceptibility')
plt.show()