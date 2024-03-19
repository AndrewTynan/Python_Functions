

# DEFINE group_by_summarise 

def group_by_summarise(df, group_by, metric, stat): 

    col_name = "{metric}_{stat}".format(metric = metric, stat = stat)
    print(col_name)

    df = (df
            .groupby([group_by])
            .agg(stat  = (metric, stat))
            .reset_index() 
            .rename(columns = {'stat': col_name}))
     
    return df 

group_by_summarise(df       = new_subs_user_level, 
                   group_by = 'is_longterm_ucg', 
                   metric   = 'user_id',
                   stat     =  'count')


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


print('The table below shows summary stats UCG and non-UCG using the field longterm_ucg_grp')

five_num_sum_by_group(new_subs_w_ucg, 'longterm_ucg_grp', 'daily_percent') 


pd.options.display.float_format = '{:.1f}'.format    
(new_subs_user_level 
    .groupby(['start_date', 'is_longterm_ucg']) 
    .agg(user_id_count  = ('user_id', 'count')) 
    .pipe(five_num_sum_by_group, 'is_longterm_ucg', 'user_id_count')) 



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



print('The table below shows 1 Month Retention summary stats UCG and non-UCG')

vars = ['longterm_ucg_grp', 'month_1_churn']
five_num_sum_by_group(new_subs_w_ucg_w_1month_churn_, vars, 'ucg_retention_rate') 






