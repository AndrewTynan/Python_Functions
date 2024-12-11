
def group_by_summarise(df, group_by, metric, stat): 

    col_name = "{metric}_{stat}".format(metric = metric, stat = stat)
    print(col_name)

    df = (df
            .groupby([group_by])
            .agg(stat  = (metric, stat))
            .reset_index() 
            .rename(columns = {'stat': col_name}))
     
    return df 


# example 
group_by_summarise(df       = monthly_mex_food_df, 
                   group_by = 'food', 
                   metric   = 'counts',
                   stat     =  'max')
