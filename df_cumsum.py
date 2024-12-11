
# NOTE: there are several examples before the df_cumsum.py function which combines the functionality of the prior examples 


##################################
##### Manual Cumulative Sum ######
##################################

df = pd.DataFrame({'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
                   'Value': [10, 20, 30, 40, 50, 60]}) 
df

# manual hardcoded way 
df['Cumulative Sum'] = df.groupby('Category')['Value'].cumsum()
df 


#################################
####### a basic function ########
#################################

def df_cumsum_basic(df, var):
    # df = df.sort_values(by=by) # would need to add a groupby
    var_name = var + " CumuSum"
    df[var_name] = df[var].cumsum()
    return df 

df_cumsum_basic(df, "Value")     


#################################
#### a function w/ groupby ######
#################################

# function to cumsum by group 
# Note: but not sorting by a column

def df_cumsum_by(df, by, var): 
    var_name = var + " CumuSum by " + by
    df[var_name] = df.groupby(by)[var].cumsum()
    return df 

df_cumsum_by(df, "Category", "Value")


################################################
#### using pipe to chain operations to chain ###
################################################

# NOTE: this example combines each of the 2 functions above 

# re-create a sample DataFrame, otherwise we are using the df which already has both cumsum columns
# so we cannot be sure this code is working correctly 

df = pd.DataFrame({'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
                    'Value': [10, 20, 30, 40, 50, 60]}) 

(df
.pipe(df_cumsum_basic, var="Value")
.pipe(df_cumsum_by,    by="Category", var="Value")
)


#################################
########### df_cumsum ###########
#################################

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


# example 
df_cumsum(monthly_mex_food_df, var = 'counts', sort = 'months')


# example 
df_cumsum(monthly_mex_food_df, var = 'counts', by = "food", sort = 'months')


# example 
# piping with the new df_cumsum() function which combines the 
(monthly_mex_food_df
.pipe(df_cumsum,    var="counts")
.pipe(df_cumsum,    var='counts', by="food") 
# .pipe(df_cumsum,    var='counts', by="food", sort = 'months') # since adding this sorts the DataFrame it makes it harder to see that the previous two approaches worked correctly
)

