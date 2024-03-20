new_subs_user_level_2023_06 = new_subs_user_level.query("start_month == '2023-06'")

cohort = (new_subs_user_level_2023_06
            .query("lifetime_month > 0") 
            .agg(count = ('user_id', 'count'))) 

retained_cohort = (new_subs_user_level_2023_06
                    .query("lifetime_month > 0") 
                    .groupby(['lifetime_month']) 
                    .agg(churned_count = ('user_id', 'count'))
                    .assign(cohort               = 218536,
                            churned_count_cumsum = lambda x: x['churned_count'].cumsum(), 
                            churn_cumsum         = lambda x: ((x['churned_count_cumsum'] / x['cohort']) * 100).round(2),
                            re_rate              = lambda x: ((x['churned_count'] / x['cohort']) * 100).round(2))
                    .reset_index()) 
retained_cohort 
# new_subs_user_level_2023_06.head()


# new_subs_user_level_2023_06 = new_subs_user_level.query("start_month == '2023-06'")

cohort = (new_subs_user_level
            .query("lifetime_month > 0") 
            .agg(count = ('user_id', 'count'))) 

retained_cohort = (new_subs_user_level_2023_06
                    .query("lifetime_month > 0") 
                    .groupby(['lifetime_month']) 
                    .agg(churned_count = ('user_id', 'count'))
                    .assign(cohort               = 218536,
                            churned_count_cumsum = lambda x: x['churned_count'].cumsum(), 
                            churn_cumsum         = lambda x: ((x['churned_count_cumsum'] / x['cohort']) * 100).round(2),
                            re_rate              = lambda x: ((x['churned_count'] / x['cohort']) * 100).round(2))
                    .reset_index()) 
retained_cohort 
# new_subs_user_level_2023_06.head()


new_subs_user_level['lifetime_month'].unique().tolist()


is_group_member_cohort = (new_subs_user_level
                            .groupby(['is_group_member']) 
                            .agg(count = ('user_id', 'count')) 
                            .reset_index()) 
is_group_member_cohort  


(new_subs_user_level
 .query("lifetime_month > 0") 
  .query("lifetime_month <= potential_lifetime_month")
    # .groupby(['lifetime_month','potential_lifetime_month']) 
     .groupby(['is_group_member']) 
    .agg(count = ('user_id', 'count')) 
    .reset_index()) 


is_group_member_cohort_lifetimes = (new_subs_user_level
                                    .query("lifetime_month > 0") # only filters out approx 125 users w/ odd data 
                                    .query("lifetime_month <= potential_lifetime_month")
                                    .groupby(['lifetime_month', 'is_group_member']) # lifetime_month changes as users retain longer and new cohorts are added  
                                    .agg(churn = ('user_id', 'count'))
                                    .reset_index())

df_l = (pd.merge(is_group_member_cohort_lifetimes,
                 is_group_member_cohort, 
                 on = ['is_group_member'])
           .assign(churn_rate = lambda x: ((x['churn'] / x['count']) * 100).round(3))) 


df_l['cumsum_churn_rate'] = df_l.groupby(['is_group_member'])['churn_rate'].cumsum() 
df_l['retained_rate'] = 100 - df_l['cumsum_churn_rate']

df_l.sort_values(by = ['is_group_member','lifetime_month'], ascending = True)  


(new_subs_user_level
    .query("lifetime_month > 0") 
    .groupby(['lifetime_month']) 
    .agg(user_id_count = ('user_id', 'count'))
    .reset_index()
    )#.head()   


(new_subs_user_level
    .query("lifetime_month > 0") 
    .groupby(['lifetime_month', 'is_group_member', 'is_churned']) 
    .agg(user_id_count = ('user_id', 'count'))
    .reset_index()
    )#.head() 


new_subs_agg = (new_subs_user_level
                .query("lifetime_month > 0") 
                .groupby(['start_month', 'is_group_member'])
                ["user_id"]
                .count()
                .reset_index()
                .rename(columns = {'user_id': 'cohort_count'}))

new_subs_agg 




new_subs_agg_lifetimes = (new_subs_user_level
                            .query("lifetime_month > 0") 
                            .groupby(['start_month', 'is_group_member', 'lifetime_month'])
                            ["user_id"]
                            .count() 
                            .reset_index()
                            .rename(columns = {'user_id': 'user_id_count'}))
new_subs_agg_lifetimes                            



new_subs_user_level['user_id'].agg(['nunique','count','size'])



# reverse cumsum 
# del(df_t) 
df_t = (new_subs_user_level 
        # .query("lifetime_month > 0") 
        .query("is_group_member == 'No'") 
        .groupby(['is_group_member', 'potential_lifetime_month'])  
        ["user_id"]
        .count()
        .reset_index()
        .rename(columns = {'user_id': 'user_id_count'})
        .assign(cumsum_rev = lambda x: x.loc[::-1, 'user_id_count'].cumsum())  
        ) 
df_t
# df_t['cumsum_rev'] = df_t.loc[::-1, 'user_id_count'].cumsum()[::-1]    
# df_t.groupby(by=['is_group_member', 'potential_lifetime_month']).sum().iloc[::-1].groupby(level=[0]).cumsum().iloc[::-1] 


