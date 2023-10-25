
# helper functions 
def convert_list_to_tuple(list):
    # code source: https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/
    return (*list, ) 


# create a sample DataFrame
# create a sample DataFrame
data_messy = {'Taco..Type': ['A', 'A', 'B', 'B', 'C', 'C'],
        'Value__number': [10, 20, 30, 40, 50, 60]}

data_messy = pd.DataFrame(data_messy) 
data_messy


def clean_col_names(df):
    cols = df.columns 
    new_column_names = []

    for col in cols:
        # new_col = col.replace('_', ' ')    
        new_col = re.sub(r'[^a-zA-Z0-9]', ' ', col)
        new_col = new_col.title()
        new_column_names.append(new_col)

    df.columns = new_column_names 


clean_col_names(data_messy)

data_messy


data = {'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
        'Value': [10, 20, 30, 40, 50, 60]}

df = pd.DataFrame(data) 
df


# manual hardcoded way 
df['Cumulative Sum'] = df.groupby('Category')['Value'].cumsum()
df 


# using a basic function
def df_cumsum_basic(df, var):
    # df = df.sort_values(by=by) # would need to add a groupby
    var_name = var + " CumuSum"
    df[var_name] = df[var].cumsum()
    return df 

df_cumsum_basic(df, "Value")     



# function to cumsum by group 
# Note: but not sorting by a column

def df_cumsum_by(df, by, var): 
    var_name = var + " CumuSum by " + by
    df[var_name] = df.groupby(by)[var].cumsum()
    return df 

df_cumsum_by(df, "Category", "Value")



# using pipe to chain operations to chain 

# re-create a sample DataFrame, otherwise we are using the df which already has both cumsum columns, so we cannot be sure this code is working correctly 
data = {'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
        'Value': [10, 20, 30, 40, 50, 60]}

df = pd.DataFrame(data) 

(df
.pipe(df_cumsum_basic, var="Value")
.pipe(df_cumsum_by,    by="Category", var="Value")
)



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
# monthly_mex_food_df



# function to cumsum by group 
# Note: now with the ability to sort 

def df_cumsum(df, **kwargs): # , by): # , **kwargs):

    # for key, value in kwargs.items():
    #     print("%s == %s" % (key, value)) 
    #     if key in kwargs.items() == 'var':
    #         print('y')

    # print(kwargs.items())

    # get kwargs
    if 'var' in kwargs:
        var = kwargs.get('var')

    if 'by' in kwargs:
        by = kwargs.get('by')    

    if 'sort' in kwargs:
        sort = kwargs.get('sort')   

    # conditional cumsum 
    if 'by' not in locals() and 'sort' not in locals(): 
        var_name     = var + "_cumuSum"
        df[var_name] = df[var].cumsum()
        return df 

    if 'by' in locals() and 'sort' not in locals(): 
        var_name     = var + "_CumuSum_by_" + by
        df[var_name] = df.groupby(by)[var].cumsum()
        return df 

    if 'by' in locals() and 'sort' in locals(): 
        var_name     = var + "_CumuSum_by_" + sort 
        df           = df.sort_values([by, sort])
        df[var_name] = df.groupby([by])[var].cumsum() 
        return df 

    if 'sort' in locals() and 'by' not in locals(): 
        var_name     = var + "_CumuSum_by_" + sort 
        df           = df.sort_values([sort])
        df[var_name] = df[var].cumsum() 
        return df         

# df_cumsum(monthly_mex_food_df, var = 'counts', by = "food", sort = 'months')
df_cumsum(monthly_mex_food_df, var = 'counts', sort = 'months')



# piping with the new df_cumsum() function which combines the 
(monthly_mex_food_df
.pipe(df_cumsum,    var="counts")
.pipe(df_cumsum,    var='counts', by="food") 
# .pipe(df_cumsum,    var='counts', by="food", sort = 'months') # since adding this sorts the DataFrame it makes it harder to see that the previous two approaches worked correctly
)


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



def print_col_vals(df, metric):

    print(df[metric].value_counts())
    print("\n")

    print(sorted(df[metric]))
    print("\n")

    print(pd.Series(df[metric]).sort_values(ascending=True))
    print("\n") 

#example 
print_col_vals(points_df, "points")


def print_group_and_col_vals(df, group, metric):

    print(df.groupby(group)[metric].unique()) 


#example 
print_group_and_col_vals(points_df, 'league', "points")



def group_percents(df, by):

    df_n =  (df
            .groupby(by)
            .size() 
            .reset_index()
            .rename({0: 'n'}, axis=1))

    df_n = (df_n  
            .assign(total = (df_n
                            .n
                            .sum())))

    df_n = (df_n  
            .assign(perc = (df_n['n'] / df_n['total'])))

    return df_n 

group_percents(points_df, 'league')


def tabyl_two_vars(df, var1, var2, percents="No"):

    var_names = var1 + " / " + var2

    if percents == "No":
        df = df.groupby([var1, var2]).size().reset_index().rename({0: "n"}, axis=1)

        df = (pd.pivot_table(df, values="n", index=[var1], columns=var2)
              .reset_index()
              .rename_axis(None, axis=1))
        df = df.rename({var1: var_names}, axis=1)
        df = df.style.hide() 

    elif percents == "Yes":
        df = df.groupby([var1, var2]).size().reset_index().rename({0: "n"}, axis=1)

        df = pd.crosstab(df[var1], df[var2], normalize="index").reset_index() # index, 'all', 'columns'
        df.columns.name = ''
        df = df.rename(columns={df.columns[0]: var_names})         

    return display(ip.display.HTML(df.to_html())) 

# examples 
# tabyl_two_vars(monthly_mex_food_df, "food", "months")
# tabyl_two_vars(monthly_mex_food_df, "food", "months", percents="Yes")

tabyl_two_vars(points_df, "league", "points_bucket")


print('can also chose to report percents')
tabyl_two_vars(points_df, "league", "points_bucket", percents="Yes")


def five_num_sum(df):
    
    import pandas as pd
    import numpy as np

    numeric_df = df.select_dtypes(include=np.number) 
    vars       = convert_list_to_tuple(numeric_df.columns.values) 
    base_df    = pd.DataFrame({'index': ['count', 'mean', 'std','min','25%','50%','75%','max']})
    namer      = 'five_num_sum'

    for i in vars: 
        namer = namer + '_' + i 

        d = df[i].describe() 
        d = pd.DataFrame(d) 
        d.reset_index(inplace=True) 
        base_df = pd.merge(base_df, d) 

    base_df.rename(columns = {'index':'stats'}, inplace = True)

    # print(namer) # would be nice to create a custom dynamic name using this string instead of using five_num_sum_df each time, hmm..
    global five_num_sum_df
    five_num_sum_df = base_df
    return five_num_sum_df

five_num_sum(points_df)


def five_num_sum(df):

    import pandas as pd
    import numpy as np

    d = df.select_dtypes(include=np.number).describe().transpose()
    d.reset_index(inplace=True) 
    d.rename(columns={'index':'metric'}, inplace=True)
    return d 

five_num_sum(points_df)    


# has a messy format w/ multi index headers, cannot easy read or work with it
# #.to_frame(index=False)#.to_flat_index() # these methods are in pandas 2.1.1, Bento has pandas 2.0.3 bummer 
points_df.groupby(by = ['league'], as_index=False)[['points']].describe()


# manual version 
def q1(x):
    return x.quantile(0.25)

def q3(x):
    return x.quantile(0.75)

(points_df
        .groupby(['league'])
        .agg(count  = ('points', 'count'),
            mean    = ('points', 'mean'),
            std     = ('points', 'std'),
            min     = ('points', 'min'),
            q1      = ('points', q1),
            median  = ('points', 'median'),
            q3      = ('points', q3),
            max     = ('points', 'max'),
        ).reset_index() 
        .assign(metric = 'points')
        .iloc[:,[0,9,1,2,3,4,5,6,7,8]] 
        # .insert(1, 'metric', df.pop(9)) # doesn't work in chain coz df needs to be referenced w/ pop... 
)   



def five_num_sum_by_group(df, by, metric):

    def q1(x):
        return x.quantile(0.25)

    def q3(x):
        return x.quantile(0.75)

    df = (df
            .groupby([by])
            .agg(count  = (metric, 'count'),
                mean    = (metric, 'mean'),
                std     = (metric, 'std'),
                min     = (metric, 'min'),
                q1      = (metric, q1),
                median  = (metric, 'median'),
                q3      = (metric, q3),
                max     = (metric, 'max'),
            ).reset_index() 
            .assign(metric = 'points')
            .iloc[:,[0,9,1,2,3,4,5,6,7,8]] 
        ) 

    global five_num_sum_by_group
    five_num_sum_by_group = df    
    return five_num_sum_by_group

five_num_sum_by_group(points_df, 'league', 'points') 



def five_num_sum_by_group(df, by):

    def q1(x):
        return x.quantile(0.25)

    def q3(x):
        return x.quantile(0.75)

    vars    = df.select_dtypes(include=['int', 'float']).columns.tolist() 
    base_df = pd.DataFrame(columns = [by, 'metric', 'count', 'mean', 'std','min','q1','median','q3','max'])     

    for i in vars: 

        d = (df
                .groupby([by])
                .agg(count  = (i, 'count'),
                    mean    = (i, 'mean'),
                    std     = (i, 'std'),
                    min     = (i, 'min'),
                    q1      = (i, q1),
                    median  = (i, 'median'),
                    q3      = (i, q3),
                    max     = (i, 'max'),
                ).reset_index() 
                .assign(metric = i)
                .iloc[:,[0,9,1,2,3,4,5,6,7,8]] 
            ) 

        base_df = pd.concat([base_df, d], ignore_index=True, axis=0) 

    global five_num_sum_by_group
    five_num_sum_by_group = base_df    
    return five_num_sum_by_group 

five_num_sum_by_group(points_df, 'league') 



agg_func_math = {
    'points':
    ['sum', 'mean', 'median', 'min', 'max', 'std', 'var']
}

points_df.groupby(['league']).agg(agg_func_math).round(2)



def alt_summary(df, by, var): 

    agg_func_math = {
        var:
        ['sum', 'mean', 'median', 'min', 'max', 'std', 'var']
    }

    df = df.groupby([by]).agg(agg_func_math).round(2)    
    return df 

alt_summary(points_df, 'league', 'points')  



# import sparklines

# def sparkline_str(x):
#     bins=np.histogram(x)[0]
#     sl = ''.join(sparklines(bins))
#     return sl

def alt_summary_2(df, by, var): 

    agg_func_math = {
        var:
        ['describe'] # sparkline_str
    }

    df = df.groupby([by]).agg(agg_func_math).round(2)    

    # df.columns = ['_'.join(col).rstrip('_') for col in df.columns.values]
    col_vals  = df.columns.values
    new_column_names = []
    for v in col_vals: 
        new_col = v[-1]
        new_column_names.append(new_col) 

    df.columns = new_column_names
    df.reset_index(inplace=True) 
    df = df.assign(metric = var)
    df = df.iloc[:,[0,9,1,2,3,4,5,6,7,8]] 

    return df 

alt_summary_2(points_df, 'league', 'points')  





