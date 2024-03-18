

def region_filter(df, region): 

    latam_countries = ['BRAZIL', 'COSTA_RICA', 'MEXICO','COLOMBIA', 'PERU','CAYMAN_ISLANDS',
                        'ARGENTINA', 'JAMAICA', 'GUATEMALA','ECUADOR', 'HONDURAS', 'URUGUAY',
                        'DOMINICAN_REPUBLIC','BOLIVIA', 'NICARAGUA', 'PANAMA','ANTIGUA_AND_BARBUDA', 
                        'CURACAO', 'PARAGUAY','BAHAMAS', 'VENEZUELA','BRITISH_VIRGIN_ISLANDS',
                        'TRINIDAD_AND_TOBAGO','ST_KITTS_AND_NEVIS', 'ARUBA','ST_LUCIA', 'BELIZE',
                         'BARBADOS','GRENADA', 'GUYANA', 'ANGUILLA','ST_VINCENT_AND_GRENADINES',
                        'TURKS_AND_CAICOS', 'SURINAME','DOMINICA', 'EL_SALVADOR', 'MONTSERRAT'
                        'HAITI', 'CHILE']      

    emea_countries = (df
                        .loc[df['market'].notna()]
                        .query("market not in @latam_countries & market != 'UNITED_STATES'")
                        .market
                        .unique().tolist())     

    if region == 'US':
        df = df.query("market == 'UNITED_STATES'") 

    elif region == 'LATAM':
        df = df.query("market in @latam_countries")
        
    elif region == 'EMEA':
        df = df.query("market in @emea_countries") 
        
    return df


def group_var_dist(df, region, vars, group_var): 

    # df is the dataframe 
    # region is the region 
    # group_var a string for the grouping variable; technically the 2nd grouping variable after 'date'
    
    for v in vars: 
        group_vars      = ['date', group_var] 
        group_vars_plus = group_vars + [v]

        df_n = region_filter(df, region)       

        df_base = (df_n
                    .groupby(group_vars_plus)
                    .agg(user_id_count = ('user_id', 'count'))
                    .reset_index())

        join_vars = ['date'] + [v]
        df_agg = (df_base
                    .groupby(join_vars)
                    .agg(user_id_count_total = ('user_id_count', 'sum'))
                    .reset_index())

        df_output = (pd.merge(df_base,
                                df_agg, 
                                on = join_vars) 
                        .assign(daily_percent = lambda x: (100 * (x['user_id_count'] / x['user_id_count_total'])).round(3)))

        df_output['date'] = pd.to_datetime(df_output['date']) 
        df_output['year_month'] = df_output['date'].dt.strftime('%Y_%m')             

        df_5_num_sum = five_num_sum_by_group(df_output, 
                                            [group_var] + [v], 
                                            'daily_percent')  
                                                                             
        plot = (col_plot(df_5_num_sum, group_var, 'mean', group_var, 
                         facet = "~ {var}".format(var = v),
                         text = 'mean') + 
                geom_errorbar(aes(x=group_var, ymin="mean-std", ymax="mean+std")) + 
                scale_y_continuous(labels = lambda l: ["%d%%" % (v * 1) for v in l], 
                                limits = [0, 100]) + 
                theme(figure_size = (16, 5),
                    legend_position='bottom') + 
                labs(title= "{region} Long Term Average Percent by {var}".format(region = region, var = v.replace("_", " ").title()),
                     x='')) 

        print(plot) 

 
def monthly_dist(df, region): 

    df = region_filter(df, region)    

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')
    df['year_month'] = df['date'].dt.strftime('%Y_%m')
    df['today'] = date.today() # - timedelta(days=1)

    df = (df.query("start_date < today")) 

    start_date_counts  = (df
                                .groupby(['year_month', 'date', group_var])   
                                .agg(user_id_count  = ('user_id', 'count'))
                                .reset_index()) 

    start_date_percents = (start_date_counts
                                .assign(daily_user_id_count = (start_date_counts.groupby('date')['user_id_count'].transform('sum')),
                                        daily_percent   = lambda x: ((100 * x['user_id_count'] / x['daily_user_id_count'])).round(2))) 
        
    start_year_month_counts  = (start_date_percents
                                    .groupby(['year_month', group_var])   
                                    .agg(avg_daily_percent = ('daily_percent', 'mean'))
                                    .reset_index()) 

    plot = (col_plot(start_year_month_counts, 'year_month', 'avg_daily_percent', group_var, 
                     text = 'avg_daily_percent', 
                     position = 'dodge') + 
            scale_y_continuous(labels = lambda l: ["%d%%" % (v * 1) for v in l], 
                               limits = [0, 100]) + 
            theme(figure_size = (16, 5),
                  legend_position = 'bottom') + 
            labs(title = "{region} Long Term Percent by Start Date".format(region = region),
                 x = ''))

    print(plot) 
