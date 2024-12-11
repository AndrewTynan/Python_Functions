
import pandas as pd 
import numpy as np
import random

#create another example df 
points_df = pd.DataFrame({'team': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                          'points': [18, 22, 19, 14, 14, 11, 20, 28],
                          'assists': [5, 7, 7, 9, 12, 9, 9, 4],
                          'rebounds': [11, 8, 10, 6, 6, 5, 9, 12],
                          'fouls': [11, 80, 10, 60, 6, 50, 9, 12]}) 

# add some cols to group by 
points_df['league'] = np.where(points_df['team'].isin(['A', 'B', 'C', 'D']), 'Major', 'Minor')
points_df['points_bucket'] = np.where(points_df['points'] >= 19, 'Upper', 'Lower')

points_df.head(2)

############################
##### make a dataset  ######
############################

# make a dataset 
foods = ['taco' for x in range(6)] + ['burrito' for x in range(6)]
monthly_mex_food_df = pd.DataFrame(foods)  
monthly_mex_food_df.rename(columns={0: 'food'}, inplace=True)

dates = pd.date_range('2023-01-01','2023-03-01', freq='MS').tolist() 
random.shuffle(dates) 
dates = dates * 4 

monthly_mex_food_df['months'] = dates
monthly_mex_food_df

nums = []
for i in range(12):
    n = random.randint(10, 50)
    nums.append(n)
 
monthly_mex_food_df['counts'] = nums
monthly_mex_food_df.head(3)

