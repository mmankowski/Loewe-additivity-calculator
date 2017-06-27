# to run open terminal window in location then type 'python "scriptname.py" "filename.csv" ' - "" indicates that these portions are replaced with actual file names

# import necessary libraries
import csv
import sys 
import math

# read in the file & convert "that memory" into a csv read file
f = open(sys.argv[1],'rb')
r = csv.reader(f)



# start at row 0 (first row)
i = 0
rows = []

for row in r:
	#adds an array to the list of arrays (arrays = list of variables); rows = list of lists, aka a 2D array -> defining the layout of spreadsheet
	rows.append([])
	#look at columns, but only for the current row
	for col in row:
		rows[i].append(col)
	# look at row 1, then row 2, then row 3....
	i+=1

	 
answers = []
m1 = float(rows[2][11])
m2 = float(rows[2][11])
Fa1A = float(rows[2][11])
Fa1B = float(rows[2][11])
Fa2A = float(rows[2][11])
Fa2B = float(rows[2][11])


#m constant for each experiment (does not change w/ dilutions - slope from linear regressions of log(Fa/Fu) v log(Dose) )
#notation: 1A = 1.1, 1B = 1.2, 2A = 2.1, 2B = 2.2


def helper(numerator, denominator, exponent):
	tmp = numerator/denominator
	return tmp ** (1/exponent)
	
	
def solve_equation(First1, First2, Third1, Third2, m1, m2, FU):
	first = helper(First1, First2, m1)
	second = helper(FU, 1-FU, m1)
	third = helper(Third1, Third2, m2)
	fourth = helper(FU, 1-FU, m2)
	return (first*second)+(third*fourth)

	
def equation_solver_wrapper(First1, First2, Third1, Third2, m1, m2):
	guess = .5
	step = .25
	result = 0
	
	for i in xrange(100):
		result = solve_equation(First1, First2, Third1, Third2, m1, m2, guess)
		if result > 1:
			guess -= step
		elif result < 1:
			guess += step
		else:
			break
		step = step/2		
	return guess
	
	
for row in xrange(2,12):	
	try:
		m1 = float(rows[row][8])
		m2 = float(rows[row][11])
		Fa1A = float(rows[row][9])
		Fa2A = float(rows[row][12])
		Fu1A = 1-Fa1A
		Fu2A = 1-Fa2A
			
		rows[row][14] = equation_solver_wrapper(Fa1A, Fu1A, Fa2A, Fu2A, m1, m2)
		rows[row][18] = 1 - rows[row][14]
		rows[row][22] = math.log(rows[row][18]/rows[row][14] ,10)
	except:
		rows[row][14] = "DNE"
		rows[row][18] = "DNE"
		rows[row][22] = "DNE"
	
	try:
		m1 = float(rows[row][8])
		m2 = float(rows[row][11])
		Fa1A = float(rows[row][9])
		Fa2B = float(rows[row][13])
		Fu1A = 1-Fa1A
		Fu2B = 1-Fa2B
		
		rows[row][15] = equation_solver_wrapper(Fa1A, Fu1A, Fa2B, Fu2B, m1, m2)
		rows[row][19] = 1 - rows[row][15]
		rows[row][23] = math.log(rows[row][19]/rows[row][15],10)
	except Exception as e:
		rows[row][15] = "DNE"
		rows[row][19] = "DNE"
		rows[row][23] = "DNE"
	
	try:
		m1 = float(rows[row][8])
		m2 = float(rows[row][11])
		Fa1B = float(rows[row][10])
		Fa2A = float(rows[row][12])
		Fu1B = 1-Fa1B
		Fu2A = 1-Fa2A
		
		#guess Fu
		rows[row][16] = equation_solver_wrapper(Fa1B, Fu1B, Fa2A, Fu2A, m1, m2)
		#guess Fa
		rows[row][20] = 1 - rows[row][16]
		#guess inhib
		rows[row][24] = math.log(rows[row][20]/rows[row][16],10)		
	except:
		rows[row][16] = "DNE"
		rows[row][20] = "DNE"
		rows[row][24] = "DNE"

	try:
		m1 = float(rows[row][8])
		m2 = float(rows[row][11])
		Fa1B = float(rows[row][10])
		Fa2B = float(rows[row][13])
		Fu1B = 1-Fa1B
		Fu2B = 1-Fa2B
		
		rows[row][17] = equation_solver_wrapper(Fa1B, Fu1B, Fa2B, Fu2B, m1, m2)
		rows[row][21] = 1 - rows[row][17]
		rows[row][25] = math.log(rows[row][21]/rows[row][17],10)
	except:
		rows[row][17] = "DNE"
		rows[row][21] = "DNE"
		rows[row][25] = "DNE"


with open(sys.argv[2], "wb") as f:
    writer = csv.writer(f)
    writer.writerows(rows)