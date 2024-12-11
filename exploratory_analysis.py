(df
.loc[:,['wallet_address','is_churned']]
.drop_duplicates() 
.groupby('is_churned')
.agg(churn = ('wallet_address','count')) 
.reset_index())

social_vars = ['linked_farcaster', 'linked_instagram', 'linked_twitter', 'country',	'referral_source']

for var in social_vars: 

    df = (raw_collectors_df
          .assign(is_churned = lambda x: np.where(x.churned_at_date == x.churned_at_date, 'Yes', 'No'))
          .groupby(['is_churned', var], dropna=False)
          ['wallet_address']
          .count()
          .reset_index()
          .rename(columns = {'wallet_address': 'wallet_address_count'}) 
          .assign(percent = lambda x: x.groupby('is_churned')['wallet_address_count'].transform(lambda y: (1. * y / y.sum()).round(2)) ))

    print(df) 
    print("\n")
    

collection_vars = ['file_type', 'chain_name']

for var in collection_vars: 

    df = (raw_collection_activity_df
          .groupby([var], dropna=False)
          ['wallet_address']
          .count()
          .reset_index())

    print(df) 
    print("\n")

(wallet_lifetime_days_df 
.drop_duplicates()
.groupby('lifetime_days')
.agg(wallet_count = ('min_date','count'))
.reset_index()
.pipe(lambda df_: ggplot(df_) + 
                  aes(x='lifetime_days', y='wallet_count', color="wallet_count") + 
                  geom_col() + 
                  theme_minimal() +
                  theme(figure_size = (8, 3),
                        legend_position='none') + 
                  labs(title="Wallet Lifetime Days",
                      subtitle = "Most users have lifetimes over a year")))

(wallet_engagement_df
.query("date == churned_at_date") 
.pipe(lambda df_:  
                ggplot(df_, aes(x='days_since_active')) +
                geom_histogram(binwidth=1) +
                theme_minimal() +
                theme(figure_size = (8, 3),
                      legend_position='none') + 
                scale_x_continuous(limits=(0, 25)) + 
                labs(title='Histogram of Days Since Active', 
                     subtitle = 'For Churned Wallets on their last date',
                     x='Values', 
                     y='Frequency')))

# (wallet_engagement_df
# .dropna()
# .query("churned_at_date.notna()")
# .query("wallet_address == '0x00b3d6508db5e725d9748ed6e9307552a35a2389'")
# .tail()) 

(wallet_engagement_df
.groupby('is_churned')
.agg(avg_days_since_active_7d_avg = ('days_since_active_7d_avg','mean'))
.reset_index()) 

(df 
.groupby('churned_at_date')
.agg(churn_count = ('wallet_address','count')) 
.reset_index()
.query("churned_at_date > '2024-09-01'") 
.pipe(lambda df_: ggplot(df_) + 
                  aes(x='churned_at_date', y='churn_count') + 
                  geom_col() + 
                  scale_y_continuous(labels=lambda lst: [f"{x:,.0f}" for x in lst]) +
                  theme_minimal() +
                  theme(figure_size = (8, 3),
                        axis_text_x = element_text(angle=45, ha='right'),
                        legend_position='none') + 
                  scale_x_date(date_breaks='1 day', date_labels='%Y-%m-%d') + 
                  labs(title="Churned Users by Date",
                       subtitle = "Note: there are a few data points prior to fall of September 2024.",
                        x = 'Churn Date',
                        y = 'Churned Wallet Count'))) 

(wallet_lifetime_days_df 
.drop_duplicates() 
.groupby('min_date')
.agg(new_wallet_count = ('wallet_address','nunique'))
.reset_index()
.query("min_date < '2023-11-01'")  
.pipe(lambda df_: ggplot(df_) + 
                  aes(x='min_date', y='new_wallet_count', fill="new_wallet_count") + 
                  geom_col() + 
                  theme_minimal() +
                  theme(figure_size = (8, 3),
                           legend_position='none') + 
                  scale_x_date(date_breaks='1 week', date_labels='%Y-%m-%d') + 
                  labs(title="Daily New Wallet Count",
                       subtitle = "Note: there are a few data points prior to fall of September 2024.",
                       x = 'Min Wallet Date',
                       y = 'New Wallet Count')))

(wallet_engagement_df
.pipe(lambda df_: pd.merge(df_, 
                            (df
                            .groupby(['wallet_address','date'])
                            .agg(max_number_collected = ('number_collected','max'))
                            .reset_index()),  
                           how = 'left', 
                           on = ['wallet_address','date']))
.groupby('is_churned')
.agg(avg_max_number_collected = ('max_number_collected','mean')).round(2)
.reset_index())

# linked_farcaster	linked_instagram	linked_twitter	

# make a combined linked_social from the other socail vars





# check churn by sign-up date
(wallet_engagement_df
.loc[:,['wallet_address','min_date','is_churned']]
.query("min_date <= '2023-10-01'")  
.groupby(['min_date', 'is_churned']) 
.agg(wallet_address_counts = ('wallet_address','count'))
.reset_index()
.pipe(lambda df_: ggplot(df_) +
                    aes(x='min_date', y='wallet_address_counts', fill='is_churned') + 
                    geom_bar(stat='identity') +  
                    scale_y_continuous(labels=lambda lst: [f"{x:,.0f}" for x in lst]) +
                    theme_minimal() +            
                    theme(figure_size = (8, 3),
                             legend_position='right') + 
                    # facet_wrap('~chain_name') + 
                    scale_x_date(date_breaks='2 months', date_labels='%b %Y') +       
                    labs(title='Wallet Counts by Min Date',
                         subtitle='And Churn Status',
                        x='Date',
                        y='Value',)))

(df
.groupby(['date','chain_name', 'commented']) 
.agg(wallet_address_counts = ('wallet_address','count'))
.reset_index()
.pipe(lambda df_: ggplot(df_) +
                    aes(x='date', y='wallet_address_counts', fill='commented') + 
                    geom_bar(stat='identity') +  
                    theme_minimal() +            
                    theme(figure_size = (8, 4),
                             legend_position='bottom') + 
                    facet_wrap('~chain_name') + 
                    scale_x_date(date_breaks='2 months', date_labels='%b %Y') +       
                    labs(title='Daily Wallet Counts by Chain',
                         subtitle='And Churn Status',
                         x='Date',
                         y='Value',
                         fill='Category')))

(df
.groupby(['date','chain_name', 'file_type']) 
.agg(wallet_address_counts = ('wallet_address','count'))
.reset_index()
.pipe(lambda df_: ggplot(df_) +
                    aes(x='date', y='wallet_address_counts', fill='file_type') + 
                    geom_bar(stat='identity') +  
                    theme_minimal() +            
                    theme(figure_size = (8, 6),
                             legend_position='bottom') + 
                    facet_grid('chain_name~file_type') + 
                    scale_x_date(date_breaks='6 months', date_labels='%b %Y') +       
                    labs(title='Daily Chain and File Type Transactions',
                         x='Date',
                         y='Value',
                         fill='Category')))

metric_list = ['linked_farcaster', 'linked_instagram', 'linked_twitter', 'country',	'file_type'] # 'referral_source',
group_by = ['date', 'chain_name', 'is_churned'] 

for metric in metric_list:
    group_by.append(metric)
    # facet = 'chain_name~' + metric + '+ is_churned'  # '~chain_name'
    facet = 'is_churned +' + metric + '~chain_name'  # '~chain_name'    
    title = metric.replace("_", " ").title() 
    plt = (df
            .groupby(group_by) 
            .agg(wallet_address_counts = ('wallet_address','count'))
            .reset_index()           
            .assign(is_churned_chain_name = lambda x: x.is_churned.astype('object') + "_" + x.chain_name.astype('object'))
            # .head(2)
            .pipe(lambda df_: ggplot(df_) +
                                aes(x='date', y='wallet_address_counts', fill='is_churned_chain_name') +  # fill=metric
                                geom_bar(stat='identity') +  
                                theme_minimal() +            
                                theme(figure_size = (8, 5),
                                         legend_position='right') + 
                                # facet_wrap(facet) + 
                                facet_grid(facet) + 
                                scale_x_date(date_breaks='2 months', date_labels='%b %Y') +       
                                labs(title = title + ' by Chain',
                                     subtitle='NOTE: top nested labels for x-axis are for',
                                     x='Date',
                                     y='Count',
                                     fill=title))
          )
    print(plt)
    print('\n')

(df
.groupby(['date', 'chain_name', 'referral_source', 'is_churned']) 
.agg(wallet_address_counts = ('wallet_address','count'))
.reset_index()
.pipe(lambda df_: ggplot(df_) +
                    aes(x='date', y='wallet_address_counts', fill='is_churned') + 
                    geom_bar(stat='identity') +  
                    theme_minimal() +            
                    theme(figure_size = (8, 6),
                             legend_position='bottom') + 
                    facet_grid('referral_source~is_churned') + 
                    scale_x_date(date_breaks='2 months', date_labels='%b %Y') +       
                    labs(title='Daily Activity by Referral Source',
                         x='Date',
                         y='Count',
                         fill='Category')))

(df
.groupby('date') 
.agg(event_count = ('wallet_address', 'count'),
     unique_wallets = ('wallet_address', 'nunique'))
.reset_index()
.pipe(lambda df_: pd.melt(df_, 
                          id_vars    = 'date',
                          var_name   = 'metric',    
                          value_name = 'value'))
.pipe(lambda df_: ggplot(df_) + 
                  aes(x='date', y='value', color="metric") + # group=1, 
                  geom_line() + 
                  theme_minimal() + 
                  scale_y_continuous(labels=lambda lst: [f"{x:,.0f}" for x in lst]) +
                  theme(figure_size = (8, 3),
                           legend_position='bottom') + 
                  scale_x_date(date_breaks='2 months', date_labels='%b %Y') + 
                  labs(title="Overall Daily Events")))

# file types are uniformly distributed 
(df 
.groupby(['chain_name','file_type'])
['wallet_address']
.count()
.reset_index())

# so are token_id's 
print('Note: just printing tail')
(raw_collection_activity_df
.groupby('token_id')
['wallet_address']
.count()
.reset_index()
.tail())