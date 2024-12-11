
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





