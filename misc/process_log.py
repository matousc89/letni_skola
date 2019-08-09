import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data_file = pd.read_csv('data/output.csv', delimiter=',')

opp_data = data_file.loc[data_file['winner'] == 'Better player']
est_bet_with_22 = opp_data.loc[opp_data['bettor_name'] == 'Better player']
est_bet = est_bet_with_22.loc[est_bet_with_22['bettor_value'] < 22]
sizing = est_bet['bet_size']
value = est_bet['bettor_value']
# print(sizing.values)
# print(value.values)
corr = est_bet['bet_size'].corr(est_bet['bettor_value'])
print("correlation coef: {:0.3f}".format(corr))
m, b = np.polyfit(sizing.values, value.values, 1)
print(m, b)

bettor_sizing_3 = est_bet_with_22.loc[opp_data['bet_size'] == 3]


# ax1 = est_bet.plot.scatter(x='bet_size', y='bettor_value')
est_bet.plot(kind='scatter', x='bet_size', y='bettor_value', color='Blue')
plt.tight_layout()

plt.figure(2)
plt.hist(bettor_sizing_3['bettor_value'], bins=range(15, 27))


# distribution of Better players values
plt.figure(3)
plt.hist(data_file['bettor_value'],  range(15, 27))
print(np.histogram(data_file['bettor_value'], range(15, 27)))

# distribution of 6 dice rolls
six_dice_roll = np.random.randint(low=1, high=6, size=(6, 1000000))
six_dice_hist = np.histogram(np.sum(six_dice_roll, axis=0), bins=range(6, 37))

plt.figure(4)
plt.hist(np.sum(six_dice_roll, axis=0), bins=range(6, 37))

# single dice distribution
single_dice_roll = np.random.randint(low=1, high=6, size=(1, 5))
single_dice_hist = np.histogram(np.sum(single_dice_roll, axis=0), bins=range(1, 7))

plt.figure(5)
plt.hist(np.sum(single_dice_roll, axis=0), bins=range(1, 7))

plt.show()
