

new_subs_user_level['start_year_month'] = new_subs_user_level['start_date'].dt.strftime('%Y_%m') 



df.loc[:, ["col_name"]]

ugh_df = df[(df['lifetime_month'] == lifetime_month)] 

.astype('category')


(test_df
    .groupby(['is_group_member', 'payment_period'])
    .agg(user_id_count  = ('is_retained', 'mean')))


(new_subs_user_level
    .groupby(["is_group_member"]) 
    .agg(count = ('user_id', 'count'))
    .reset_index()) 

# transform is like R's mutate 
new_subs_w_ucg['daily_total'] = (new_subs_w_ucg.
                                 groupby("seamless_paid_start_date")
                                 ["user_id_count"]
                                 .transform('sum')) 

(new_subs_user_level
    .query('lifetime_month >= 1')
    .loc[:, ['user_id', 'is_churned', 'is_group_member']]
    .head(3)) 

new_subs_user_level['M1_is_churned'] = new_subs_user_level['lifetime_month'].apply(lambda x: 1 if x > 1 else 0) 

(new_subs_user_level 
    .query('lifetime_month >= 1') 
    .groupby(['seamless_paid_start_month', 'is_group_member', 'M1_is_churned']) 
    ['user_id'] 
    .count() 
    .reset_index()).head()

(new_subs_user_level
    .query("lifetime_month > 0") 
    .groupby(['lifetime_month', 'is_group_member'])
    ["user_id"]
    .count()
    .reset_index()
    .rename(columns = {'user_id': 'user_id_count'})
    
    ).head()





# calculated column
new_subs_w_ucg = (new_subs_w_ucg
                  .rename(columns = {'user_id_count': 'daily_sub_total'})
                  .assign(daily_percent = lambda x: ((x['daily_sub_total'] / x['daily_total']) * 100).round(2)))  


# prop_test_results['huh'] = prop_test_results.apply(daily_percent = lambda x: 'True' if <= 0.05 else 'False')

prop_test_results['stat_sig'] = prop_test_results['pvalue'].apply(lambda x: 'Yes' if x <= 0.05 else 'No') 


(prop_test_results
    .assign(id=lambda df: np.where(prop_test_results["pvalue"] <= 0.05 , "Yes", "No")))



    # .assign(is_retained = lambda x: 'Yes' if x <= 0.05 else 'No') 
    # .assign(is_churned = lambda df: np.where(new_subs_user_level['lifetime_month'] > 1 , 'Yes', 'No'))
    # .assign(is_churned = lambda x: x['lifetime_month'].apply(lambda y: > 1 , 'Yes', 'No')) 


https://stackoverflow.com/questions/57609780/pandas-using-assign-and-if-else-statement-in-method-chaining

df = (df.
    assign(age_bracket= lambda x: x['age'].apply(lambda y: "under 25" if y < 25 else
        ("25-34" if y < 35 else "35+"))))
print (df)

https://www.geeksforgeeks.org/ways-to-apply-an-if-condition-in-pandas-dataframe/


new_subs_cohort_retention['retention_rate'] = new_subs_cohort_retention['retention_rate'].astype(float)
# new_subs_cohort_retention = (new_subs_cohort_retention
#                             .assign(retention_rate = lambda x: x['retention_rate'] * 100))



        # print( (df 
        #         .groupby(['is_group_member', 'is_churned']) # 'seamless_paid_start_month',
        #         ['user_id'] 
        #         .count() 
        #         .reset_index()) ) 

            # df['is_eligible_population'] = df['lifetime_month'].apply(lambda x: 'Yes' if x >= (lifetime_month - 1) 
            #                                                                 & df['potential_lifetime_month'] >= lifetime_month
            #                                                            else 'No')         


        print( (df 
                    .groupby(['is_churned'])
                    ["user_id"]
                    .count()
                    .reset_index()
                    .rename(columns = {'user_id': 'user_id_count'})) )      




    if 'position' in kwargs:
        position = kwargs.get('position')    
        plt = (ggplot(df) + 
               geom_col(position=position) + 
               aes(x = x, y = y, fill = fill))
    else: 
        plt = (ggplot(df) + 
               geom_col() + 
               aes(x = x, y = y, fill = fill)) 



    if 'facet' in kwargs:

        facet_col = kwargs.get('facet')    
        if 'nrow' in kwargs: 
            nrow = kwargs.get('nrow') 
        else: nrow = 1 

        if 'facet_scales' in kwargs: 
            facet_scales = kwargs.get('facet_scales')   # NOTE scales : Literal["fixed", "free", "free_x", "free_y"] = "fixed" 
            plt = (plt + facet_wrap(facet_col, nrow=nrow, scales=facet_scales))  
        else: 
            plt = (plt + facet_wrap(facet_col, nrow=nrow))     

                    


# fig = px.bar(monthly_cohort_counts, 
#              x='seamless_paid_start_month', 
#              y='cohort_count', 
#              color="seamless_paid_start_month", 
#              facet_col="is_group_member",
#              text_auto='.2s',
#              title="New Subscriber Monthly Counts by Long-Term UCG Status")
# fig.show()

# fig = px.bar(is_group_member_retention_rate_M1, 
#              x='is_group_member', 
#              y='mean', 
#              color="is_group_member", 
#             #  text='mean',
#              title="New Subscriber First Month Avg Retention by Long-Term UCG Status").update_traces(error_y={"type": "data",
#                                                                                                               "symmetric": False,
#                                                                                                               "array":      is_group_member_retention_rate_M1["std"],
#                                                                                                               "arrayminus": is_group_member_retention_rate_M1["std"]})
# fig.show() 


# fig = px.bar(new_subs_cohort_retention_SUMMARY, 
#              x='is_group_member', 
#              y='mean', 
#              color="is_group_member", 
#              facet_col="lifetime_month",
#              barmode='group',
#             #  text_auto='.2s',
#              title="New Subscriber Avg Monthly Retention by Long-Term UCG Status").update_traces(error_y={"type": "data",
#                                                                                                           "symmetric": False,
#                                                                                                           "array": new_subs_cohort_retention_SUMMARY["std"],
#                                                                                                           "arrayminus": new_subs_cohort_retention_SUMMARY["std"]})
# # fig.update_layout(showlegend=False)
# fig.show()

# fig = px.line(new_subs_cohort_retention, 
#               x="lifetime_month", 
#               y="retention_rate", 
#               color="seamless_paid_start_month", 
#               facet_col="is_group_member",
#               title="New Subscriber Monthly Retention Percent by Long-Term UCG Status")
# fig.show() 



(ggplot(is_group_member_retention_rate_M1) + 
    aes(x = 'is_group_member', y = 'mean', fill = 'is_group_member') + 
    geom_col() + 
    geom_errorbar(aes(x="is_group_member", ymin="mean-std", ymax="mean+std")) + 
    geom_text(aes(label = 'mean'), format_string="{:.2f}%", size = 8, va="bottom", nudge_y = 10) + 
    scale_y_continuous(limits = (0,100)) + #  labels=percent_format()
    theme(figure_size = (12, 4),
          legend_position='bottom') + 
    labs(title="New Subscriber First Month Avg Retention by Long-Term UCG Status",
         x='')) 

lifetime_months_var = f"lifetime_month == {2}" 
lifetime_months_var    

(new_subs_cohort_retention
    .query(lifetime_months_var) 
    .query("seamless_paid_start_month == '2023-06'") 
    .loc[:, ['lifetime_month', 'is_group_member', 'cohort_count', 'retained_count', ]] 
    .groupby(['lifetime_month', 'is_group_member'])
    .agg(cohort_count_total  = ('cohort_count', 'sum'),
        retained_count_total = ('retained_count', 'sum'))
    .reset_index() 
    .assign(retention_rate = lambda x: ((x['retained_count_total'] / x['cohort_count_total']) * 100).round(3)))    



(ggplot(new_subs_cohort_retention) + 
    aes(x = 'lifetime_month', y = 'retention_rate', fill = 'is_group_member') + 
    facet_wrap(' ~ start_month', scales='free') + 
    geom_col(position='dodge') + 
    scale_y_continuous(limits = (0,100)) + # , labels=percent_format()
    geom_text(aes(label = 'retention_rate'), position = position_dodge(width = 1), format_string="{:.0f}%", size = 8, va="bottom") + 
    theme(figure_size = (16, 6),
          legend_position='bottom') + 
    labs( x= '') + 
    labs(title = 'Montly Retention by Cohort Month & Long-Term UCG Status',
         subtitle = 'For New Subs in the US'))  


(ggplot(monthly_cohort_counts) + 
    aes(x = 'start_month', y = 'cohort_count', fill = 'start_month') + 
    facet_wrap(' ~ is_group_member') + 
    geom_col() + 
    scale_y_continuous(labels = comma_format(),
                       limits = [0, 800000]) +   
    geom_text(aes(label = 'cohort_count'), size = 10, va="bottom", format_string="{:,}") +  
    theme(figure_size = (12, 4),
          legend_position='bottom') + 
    labs(title="New Subscriber Monthly Counts by Long-Term UCG Status")) 


(ggplot(new_subs_cohort_retention_SUMMARY) + 
    aes(x = 'is_group_member', y = 'mean', fill = 'is_group_member') + 
    geom_col() + 
    geom_errorbar(aes(x="is_group_member", ymin="mean-std", ymax="mean+std")) + 
    geom_text(aes(label = 'mean'), format_string="{:.0f}%", size = 8, va="top", nudge_y = 15) + 
    facet_wrap("lifetime_month", nrow=1) + 
    theme(figure_size = (16, 4),
          legend_position='bottom') + 
    labs(title="New Subscriber First Month Avg Retention by Long-Term UCG Status",
         x='')) 


        # if groups == 'basic': 
        #     groups = ['lifetime_month_ref', 'is_group_member']
        # elif groups == 'detailed':
        #     groups = ['lifetime_month_ref', 'is_group_member', 'tier_type', 'payment_provider'] 






