
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


## Example
# add execcfile to dexample data 

group_percents(points_df, 'league')
