# examples of chaining 

https://www.kdnuggets.com/2021/01/cleaner-data-analysis-pandas-pipes.html


(new_subs_cohort_retention
    .query('lifetime_month == 1')
    .groupby(['is_group_member'])
    ["cohort_count"]
    .sum()
    .reset_index()) 


df_agg = (df
        .groupby(["start_date", "longterm_ucg_grp"])
        ["user_id_count"]
        .sum()
        .reset_index()) 


user_level = (user_level 
                .assign(is_churned = lambda df: np.where(user_level["terminated_date"].notnull(), 1, 0))) 


monthly_cohort_counts_ul = (user_level
                            .query('lifetime_month == 1')
                            .loc[:,['start_month', 'is_group_member', 'cohort_count']]
                            .reset_index())


df_chain = (
    pd.read_csv('https://raw.githubusercontent.com/flyandlure/datasets/master/ecommerce_sales_by_date.csv')
    .fillna('')
    .sort_values(by='date', ascending=False)
    .assign(
        conversion_rate=(lambda x: ((x['transactions'] / x['sessions']) * 100).round(2)),
        revenuePerTransaction=(lambda x: x['revenuePerTransaction'].round(2)),
        transactionsPerSession=(lambda x: x['transactionsPerSession'].round(2))
    )
    .rename(columns={'date': 'Date', 
                    'sessions': 'Sessions', 
                    'transactions': 'Transactions', 
                    'transactionRevenue': 'Revenue', 
                    'transactionsPerSession': 'Transactions Per Session', 
                    'revenuePerTransaction': 'AOV',
                    'conversion_rate': 'CR'})        
    .drop(columns=['Unnamed: 0', 'Transactions Per Session'])
    .astype({'Date': 'datetime64[ns]'})  
)



# https://tomaugspurger.net/posts/method-chaining/

def read(fp):
    df = (pd.read_csv(fp)
            .rename(columns=str.lower)
            .drop('unnamed: 36', axis=1)
            .pipe(extract_city_name)
            .pipe(time_to_datetime, ['dep_time', 'arr_time', 'crs_arr_time', 'crs_dep_time'])
            .assign(fl_date=lambda x: pd.to_datetime(x['fl_date']),
                    dest=lambda x: pd.Categorical(x['dest']),
                    origin=lambda x: pd.Categorical(x['origin']),
                    tail_num=lambda x: pd.Categorical(x['tail_num']),
                    unique_carrier=lambda x: pd.Categorical(x['unique_carrier']),
                    cancellation_code=lambda x: pd.Categorical(x['cancellation_code'])))
    return df


(df.dropna(subset=['dep_time', 'unique_carrier'])
   .loc[df['unique_carrier']
       .isin(df['unique_carrier'].value_counts().index[:5])]
   .set_index('dep_time')
   # TimeGrouper to resample & groupby at once
   .groupby(['unique_carrier', pd.TimeGrouper("H")])
   .fl_num.count()
   .unstack(0)
   .fillna(0)
   .rolling(24)
   .sum()
   .rename_axis("Flights per Day", axis=1)
   .plot()
)
sns.despine()



flights = (df[['fl_date', 'tail_num', 'dep_time', 'dep_delay']]
           .dropna()
           .sort_values('dep_time')
           .loc[lambda x: x.dep_delay < 500]
           .assign(turn = lambda x:
                x.groupby(['fl_date', 'tail_num'])
                 .dep_time
                 .transform('rank').astype(int)))

fig, ax = plt.subplots(figsize=(15, 5))
sns.boxplot(x='turn', y='dep_delay', data=flights, ax=ax)
ax.set_ylim(-50, 50)
sns.despine()


plt.figure(figsize=(15, 5))
(df[['fl_date', 'tail_num', 'dep_time', 'dep_delay']]
    .dropna()
    .assign(hour=lambda x: x.dep_time.dt.hour)
    .query('5 < dep_delay < 600')
    .pipe((sns.boxplot, 'data'), 'hour', 'dep_delay'))
sns.despine()




# https://medium.com/@ulriktpedersen/modern-pandas-streamlining-your-workflow-with-method-chaining-f65e75deb193

# Read in the data from a CSV file and filter the data to include only sales from the last year
df = (pd.read_csv('sales_data.csv')
      .query('year == 2022')
      .reset_index(drop=True)
     )

# Group the data by region and sum the sales, then filter the regions with sales above a certain threshold
high_sales_regions = (df
                      .groupby('region')
                      .agg({'sales': 'sum'})
                      .reset_index()
                      .query('sales > 1000000')
                      .reset_index(drop=True)
                     )

# Merge the high sales regions back into the original data, sort the data by region and month
df = (df
      .merge(high_sales_regions, on='region', how='inner')
      .sort_values(by=['region', 'month'], ascending=[True, False])
     )

# Calculate the monthly average sales for each region and pivot the data to get a summary table
summary_table = (df
                 .groupby(['region', 'month'])
                 .agg({'sales': 'mean'})
                 .reset_index()
                 .pivot(index='region', columns='month', values='sales')
                 .fillna(0)
                )


data['daily_total'] = (data
                     .groupby(["start_date", "grp"])
                     ["user_id_count"]
                     .transform('sum')) 



