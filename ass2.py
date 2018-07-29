import numpy as np
import numpy.random as rnd
import random
import collections
from decimal import *
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1 import ImageGrid

index_board = {0:'GO', 1:'MEDITER-RANEAN AVENUE', 2:'COMMUNITY CHEST', 3:'BALTIC AVENUE', 4:'INCOME TAX', 
5:'READING RAILROAD', 6:'ORIENTAL AVENUE', 7:'CHANCE', 8:'VERMONT AVENUE', 9:'CONNECTICUT AVENUE', 
10:'JAIL', 11:'ST.CHARLES PLACE', 12:'ELECTRIC COMPANY', 13:'STATES AVENUE', 14:'VIRGINIA AVENUE',
15:'PENNSYLVANIA RAILROAD', 16:'ST.JAMES PLACE', 17:'COMMUNITY CHEST', 18:'TENNESSEE AVENUE', 19:'NEW YORK AVENUE',
20:'FREE PARKING', 21:'KENTUCKY AVENUE', 22:'CHANCE', 23:'INDIANA AVENUE', 24:'ILLINOIS AVENUE',
25:'B&O RAILROAD', 26:'ATLANTIC AVENUE', 27:'VENTNOR AVENUE', 28:'WATER WORKS', 29:'MARVIN GARDENS',
30:'GO TO JAIL', 31:'PACIFIC AVENUE', 32:'NORTH CAROLINA AVENUE', 33:'COMMUNITY CHEST', 34:'PENNSYLVANIA AVENUE',
35:'SHORT LINE', 36:'CHANCE', 37:'PARK PLACE', 38:'LUXURY TAX', 39:'BOARDWALK'}

#for the card not related to movement, set them all to stay, keep the probability as the real life
chance = ['STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'GO TO JAIL', 
'GO', 'ST.CHARLES PLACE', 'ILLINOIS AVENUE', 'BOARDWALK', 'READING RAILROAD', 
'NEAREST UTILITY', 'SPACES BACK', 'NEAREST RAILROAD']
#suppose the advanced somewhere is to ventor avenue
community = ['STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'GO TO JAIL', 
'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'STAY', 'ADVANCED']

def roll_dice(board, pos, n, count_move):
	d1, d2 = rnd.randint(1, 6+1, 2)    # roll two dices, value 1 to 6
	count_move = count_move + 1
	if(d1 == d2) & (n <= 3):    #doubling rule
		result = count_pos(board, pos, d1+d2, count_move)
		next_pos = result[0]
		if result[1] == count_move:	#check if went to the jail, because the count_move will only change in the roll_dice() function and the jail_condition() function, if the count_move changed, which means the player went into the jail
			return roll_dice(board, next_pos, n+1, count_move)
	elif n > 3:  #go to jail case
		next_pos = 10
		return jail_condition(board, next_pos, 1, count_move)
	
	result = count_pos(board, pos, d1+d2, count_move)
	return result  # eg. result = [position, count_move]


def jail_condition(board, pos, n, count_move):
	board[pos] = board[pos] + 1
	d1, d2 = rnd.randint(1, 6+1, 2)
	count_move = count_move + 1
	if(d1 == d2):   #if equal, then good to get out
		return count_pos(board, pos, d1, count_move)
	elif(n <= 3):  #roll again
		return jail_condition(board, pos, n+1, count_move)
	else:  #now still get out with a movement = d1+d2
		return count_pos(board, pos, d1+d2, count_move)


def count_pos(board, current_pos, move, count_move):
	next_pos = current_pos + move
	if next_pos > 39:   #if it is already gone one circle, which means the index > 39, now should return to GO, then adjust the index
		next_pos = next_pos - 40
	position = next_pos
	#check if go to gail	
	if index_board[next_pos] == 'GO TO JAIL':
		result = jail_condition(board, next_pos, 1, count_move)
		next_pos = result[0]
		count_move = result[1]

	elif index_board[next_pos] == 'JAIL':
		result = jail_condition(board, next_pos, 1, count_move)
		next_pos = result[0]
		count_move = result[1]

	#check if is in the CHANCE square
#	position = next_pos
	elif index_board[next_pos] == 'CHANCE':
		rand_chance = random.choice(chance)
		#check what the chance card is
		if rand_chance == 'ST.CHARLES PLACE':
			next_pos = 11
		elif rand_chance == 'ILLINOIS AVENUE':
			next_pos = 24
		elif rand_chance == 'BOARDWALK':
			next_pos = 39
		elif rand_chance == 'READING RAILROAD':
			next_pos = 5
		elif rand_chance == 'NEAREST UTILITY':  # go to the electric company or water works
			if next_pos - 12 > next_pos - 28:
				next_pos = 28
			else:
				next_pos = 12
		elif rand_chance == 'NEAREST RAILROAD': # go to the nearest railroad
			if next_pos - 5 > next_pos - 15:
				if next_pos - 15 > next_pos - 25:
					next_pos = 25
				else:
					next_pos = 15
			else:
				if next_pos - 5 > next_pos - 25:
					next_pos = 25
				else:
					next_pos = 5
		elif rand_chance == 'SPACES BACK':  # return 3 spaces back
			board[position] = board[position] + 1  
			next_pos = next_pos - 3
			if next_pos < 0:
				next_pos = 40 + next_pos
		elif rand_chance == 'GO TO JAIL':
			result = jail_condition(board, next_pos, 1, count_move)
			next_pos = result[0]
			count_move = result[1]

	#check if is in the COMMUNITY CHEST square
	elif index_board[next_pos] == 'COMMUNITY CHEST':
		rand_chance = random.choice(community)
		if rand_chance == 'ADVANCED':
			next_pos = random.randint (0,39)
		elif rand_chance == 'GO TO JAIL':
			result = jail_condition(board, next_pos, 1, count_move)
			next_pos = result[0]
			count_move = result[1]
	
	if position != next_pos:
		board[position] = board[position] + 1 

	board[next_pos] = board[next_pos] + 1  
	return (next_pos, count_move)


avg_prob_board = collections.OrderedDict()
prob_board = collections.OrderedDict()
total_board = collections.OrderedDict()
avg_total = collections.OrderedDict()
getcontext().prec = 5
for i in range(40):
	prob_board[index_board[i]] = Decimal(0)
	total_board[index_board[i]] = Decimal(0)

for i in range(1000):
	#assign a index value to each square eg. 0 for GO, 1 for MEDITER-RANEAN AVENUE, 2 for COMMUNITY CHEST, 3 for BALTIC AVENUE
	board = {}
	for i in range(40):
		board[i] = 0  #initial value = 0
	
	position = 0
	count_move = 0  #counts the number of movements
	while count_move < 100:
		result = roll_dice(board, position, 0, count_move)
		position = result[0]
		count_move = result[1]

	# now count the probability for each square space in the case of 100 movements
	for j in range(40):
		prob_board[index_board[j]] = prob_board[index_board[j]] + Decimal(board[j])/Decimal(100)
		total_board[index_board[j]] = total_board[index_board[j]] + board[j]

#	print board
#	print prob_board

for element in prob_board:
	avg_prob_board[element] = prob_board[element]/Decimal(1000)
	avg_total[element] = total_board[element]/Decimal(1000)

print avg_prob_board
print avg_total

#------------------------------------------------Visualization-----------------------------------------------------#
beacon = np.array([[20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0],
	      [19.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 31.0],
          [18.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 32.0],
          [17.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 33.0],
          [16.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 34.0],
          [15.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 35.0],
          [14.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 36.0],
          [13.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 37.0],
          [12.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 38.0],
          [11.0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 39.0],
          [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0]])

board_show = np.array([['FP,0.024', 'KA,0.024', 'CH,0.03', 'INA,0.022', 'ILA,0.026', 'BR,0.027', 'AA,0.022', 'VA,0.022', 'WW,0.027', 'MG,0.020', 'GJ,0.104'],
	['NA,0.026', '', '', '', '', '', '', '', '', '', 'PA,0.026'],
	['TA,0.024', '', '', '', '', '', '', '', '', '', 'NCA,0.026'],
	['COMMUNITY CHEST', '', '', '', '', '', '', '', '', '', 'CC,0.043'],
	['SJP,0.028', '', '', '', '', '', '', '', '', '', 'PA,0.028'],
	['PR,0.028', '', '', '', '', '', '', '', '', '', 'SL,0.029'],
	['VA,0.027', '', '', '', '', '', '', '', '', '', 'CH,0.03'],
	['SA,0.028', '', '', '', '', '', '', '', '', '', 'PP,0.025'],
	['EC,0.027', '', '', '', '', '', '', '', '', '','LT,0.025'],
	['SCP,0.028', '', '', '', '', '', '', '', '', '', 'BW,0.028'],
	['JAIL,0.11', 'CA,0.024', 'VA,0.024', 'CH,0.03', 'OA,0.023', 'RR,0.026', 'IT,0.024', 'BA,0.023', 'CC,0.046', 'MA,0.022', 'GO,0.023']])

fig, ax = plt.subplots()
im = ax.imshow(beacon)
ax.set_xticks(np.arange(11))
ax.set_yticks(np.arange(11))

for i in range(11):
    for j in range(11):
        text = ax.text(j, i, board_show[i, j],
                       ha="center", va="center", color="w", size = 5)
plt.axis('off')
plt.show()


board_name = np.array([['FREE PARKING', 'KENTUCKY AVENUE', 'CHANCE', 'INDIANA AVENUE', 'ILLINOIS AVENUE', 'B&O RAILROAD', 'ATLANTIC AVENUE', 'VENTNOR AVENUE', 'WATER WORKS', 'MARVIN GARDENS', 'GO TO JAIL'],
	['NEW YORK AVENUE', '', '', '', '', '', '', '', '', '', 'PACIFIC AVENUE'],
	['TENNESSEE AVENUE', '', '', '', '', '', '', '', '', '', 'NORTH CAROLINA AVENUE'],
	['COMMUNITY CHEST', '', '', '', '', '', '', '', '', '', 'COMMUNITY CHEST'],
	['ST.JAMES PLACE', '', '', '', '', '', '', '', '', '', 'PENNSYLVANIA AVENUE'],
	['PENNSYLVANIA RAILROAD', '', '', '', '', '', '', '', '', '', 'SHORT LINE'],
	['VIRGINIA AVENUE', '', '', '', '', '', '', '', '', '', 'CHANCE'],
	['STATES AVENUE', '', '', '', '', '', '', '', '', '', 'PARK PLACE'],
	['ELECTRIC COMPANY', '', '', '', '', '', '', '', '', '','LUXURY TAX'],
	['ST.CHARLES PLACE', '', '', '', '', '', '', '', '', '', 'BOARDWALK'],
	['JAIL', 'CONNECTICUT AVENUE', 'VERMONT AVENUE', 'CHANCE', 'ORIENTAL AVENUE', 'READING RAILROAD', 'INCOME TAX', 'BALTIC AVENUE', 'COMMUNITY CHEST', 'MEDITER-RANEAN AVENUE', 'GO']])


