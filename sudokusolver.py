# sudoku solver
import sys

def solve(f):
	puzzle = import_puzzle(f)
	print_puzzle(puzzle)
	while True :
		for i in range(0, len(puzzle)):			
			for j in range(0, len(puzzle[i])):	
				if type(puzzle[i][j]) == list:					
					puzzle[i][j] = [x for x in puzzle[i][j] if x not in hline(puzzle, i)]
					puzzle[i][j] = [x for x in puzzle[i][j] if x not in vline(puzzle, j)]
					puzzle[i][j] = [x for x in puzzle[i][j] if x not in square(puzzle, i, j)]
					if len(puzzle[i][j]) == 1:
						puzzle[i][j] = int(puzzle[i][j][0])
					print(puzzle[i][j])
		#print_puzzle(puzzle)		
		if isSolved(puzzle):
			break;
	print_puzzle(puzzle)	

def import_puzzle(f):
	file_puzzle =  file(f)
	puzzle = []	
	for line in file_puzzle:		
		#remove the EOL character
		if line[-1] == "\n":
			line = line[0:len(line) - 1]
		#add white spaces at the end of the string if too short
		if len(line) > 9:
			line = line[0:9]
		if len(line) < 9:
			line = add_white_spaces(line)		
		pl = []
		for c in line:
			if c == " ":
				pl.append(range(1,10));
			else:	
				pl.append(int(c))
		puzzle.append(pl)
	return puzzle

def isSolved(puzzle):	
	for row in puzzle:
		for element in row:			
			if type(element) == list:
				return False
	return True

def hline(puzzle, rowIndex):
	res = []
	for element in puzzle[rowIndex]:
		if type(element) == int:
				res.append(element)
	return res

def vline(puzzle, colIndex):
	res = []
	for rowIndex in range(0,len(puzzle[colIndex])):	
			element =  puzzle[rowIndex][colIndex]
			if type(element) == int:
				res.append(element)
	return res

def square(puzzle, col, row):	
	result = []
	for col_shift in range(3):
		for row_shift in range(3):
			element = puzzle[base(col) + col_shift][base(row) + row_shift]
			if type(element) == int:
				result.append(element)
	return result

def base(index):
	if index >= 6:
		return 6
	elif index >= 3:
		return 3
	else:
		return 0

def add_white_spaces(line):
	return line + " " * (9 - len(line))

def print_puzzle(puzzle):
	separator = "__" * (len(puzzle[0]) + 1)
	print separator	
	for line in puzzle:		
		out =  "|"  
		for element in line:
			 if type(element) == int:
			 	out += str(element) + " " 
			 else:
			 	out += "X "			
		out +=  "|"
		print out
	print separator

#print import_puzzle("puzzle2.txt")
solve(sys.argv[1])