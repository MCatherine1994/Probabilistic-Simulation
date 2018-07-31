### **Request**:  
  * Simulating a game of Monopoly to experimentally determine the cummulative probability of landing on each square following the rules of the game after 100 moves. To get accurate probabilities you will have to run 1000 simulated games.  
  * Only considering a single player and ignoring buying/selling property. Simulate chance cards, rolling the dice including doubles, and going to jail.  
  * Considering the problem of generating a random sample from a specified distribution on a single variable. You can assume that a random number generator is available that returns a random number uniformly distributed between 0 and 1. Let X be a discrete variable with P(X = xi) = pi for i 1, ..., k. The cummulative distribution of X gives the probability X x1, ..., xj for each possible j.  
  * Visualizing the board and associated probabilities in color.  
### **Note**:
#### **[Install jupyter notebook](http://jupyter.org/install)**  
#### **[Sample for random variable](https://connex.csc.uvic.ca/access/content/group/7961b163-7f3f-42e5-bb82-d17069d39906/Notebooks/data_mining_random_variables.ipynb)**

#### **Generate random variables**:
```
import numpy.random as rnd
d1, d2 = rnd.randint(1, 6+1, 2)    # roll two dices, value 1 to 6
```
#### **Visualization**:
```
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

//assign different color on board area and assign white color to the middle part
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
```
