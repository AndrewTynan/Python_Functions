

# has a messy format w/ multi index headers, cannot easy read or work with it
# #.to_frame(index=False)#.to_flat_index() # these methods are in pandas 2.1.1, Bento has pandas 2.0.3 bummer 
points_df.groupby(by = ['league'], as_index=False)[['points']].describe()



# DEFINE 
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
            .assign(metric = metric)
            ) 

    return df


print('The table below shows summary stats  and non- using the field longterm__grp')

five_num_sum_by_group(new_subs_w_, 'longterm__grp', 'daily_percent') 


pd.options.display.float_format = '{:.1f}'.format    
(new_subs_user_level 
    .groupby(['start_date', 'is_longterm_']) 
    .agg(user_id_count  = ('user_id', 'count')) 
    .pipe(five_num_sum_by_group, 'is_longterm_', 'user_id_count')) 



# DEFINE 
def five_num_sum_by_group(df, by, metric):

    if len(by) > 1: 
        pass 
    else: 
        by = list(by)

    def q1(x):
        return x.quantile(0.25)

    def q3(x):
        return x.quantile(0.75)

    df = (df
            .groupby(by)
            .agg(count  = (metric, 'count'),
                mean    = (metric, 'mean'),
                std     = (metric, 'std'),
                min     = (metric, 'min'),
                # q1      = (metric, q1),
                median  = (metric, 'median'),
                # q3      = (metric, q3),
                max     = (metric, 'max'),
            ).reset_index() 
            .assign(metric = metric)
            ) 

    return df



print('The table below shows 1 Month Retention summary stats  and non-')

vars = ['longterm__grp', 'month_1_churn']
five_num_sum_by_group(new_subs_w__w_1month_churn_, vars, '_retention_rate') 


######################
# alternate approach #
######################

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


# example
# add execcfile to example data 

five_num_sum(points_df)



######################
# alternate approach #
######################


def five_num_sum(df):

    import pandas as pd
    import numpy as np

    d = df.select_dtypes(include=np.number).describe().transpose()
    d.reset_index(inplace=True) 
    d.rename(columns={'index':'metric'}, inplace=True)
    return d 

# example 
five_num_sum(points_df)    


######################
# alternate approach #
######################

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


# example 
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





