
df_agg_results['lifetime_month'] = np.where(df_agg_results['lifetime_month_ref']==1, 'one',
                                    np.where(df_agg_results['lifetime_month_ref']==2, 'two',
                                    np.where(df_agg_results['lifetime_month_ref']==3, 'three',
                                    np.where(df_agg_results['lifetime_month_ref']==4, 'four',
                                    np.where(df_agg_results['lifetime_month_ref']==5, 'five',
                                    np.where(df_agg_results['lifetime_month_ref']==6, 'six',
                                    np.where(df_agg_results['lifetime_month_ref']==7, 'seven',
                                    np.where(df_agg_results['lifetime_month_ref']==8, 'eight',
                                             'nine'))))))))
# df_agg_results

df_agg_results['lifetime_month_ref'] = df_agg_results['lifetime_month_ref'].astype('category')


(col_plot(df_agg_results, 'lifetime_month', 'retention_rate', 'is_longterm_ucg', 
          text = 'retention_rate', 
          percent = 'retention_rate',
        #   facet = 'lifetime_month_ref', 
        # facet_scales = 'free',        
          position = 'dodge',
          percent_deciamls = 1,
        #   nudge_y = 10
          ) + 
theme(figure_size = (16, 4),
      legend_position='bottom') + 
labs(title="Average Long Term UCG Percent by Month"))



(col_plot(new_subs_cohort_retention_SUMMARY, x = 'is_group_member', y = 'mean', fill = 'is_group_member',  
          text = 'mean', 
          percent = 'mean',
          facet = 'lifetime_month', 
          facet_scales = 'free',
          position = 'dodge',
          text_size = 8,
          percent_deciamls = 0,
          nudge_y = 8) + 
geom_errorbar(aes(x="is_group_member", ymin="mean-std", ymax="mean+std")) +  
theme(figure_size = (16, 4),
      legend_position='bottom') + 
labs(title = 'New Subscriber First Month Avg Retention by Long-Term  Status',
     subtitle = 'For New Subs in the US',
     x= '')) 



#####################################
####### Plotting Test Results #######
#####################################

(col_plot(t_test_agg_results, 'factor(lifetime_month)', 'retention_rate', 'is_group_member', 
          text = 'retention_rate', 
          percent = 'retention_rate',   
          position = 'dodge',
          percent_deciamls = 1) + 
theme(figure_size = (16, 4),
      legend_position='bottom') + 
labs(title="Cumulative Retention by Long Term  Status Lifetime Month",
     x = 'Lifetime Month')) 


(col_plot(t_test_agg_results, 'factor(lifetime_month)', 'retention_rate', 'is_group_member', 
          text = 'retention_rate', 
          percent = 'retention_rate', 
          position = 'dodge',
          percent_deciamls = 1) + 
theme(figure_size = (16, 4),
      legend_position='bottom') + 
labs(title="Prior Month Retention by Long Term  Status Lifetime Month",
     subtitle='Note: the large drop in month 4 is due to the large November cohort',
     x = 'Lifetime Month')) 


(plot_col(anova_tier_type_df_agg_results, 
          'factor(lifetime_month_ref)', 
          'retention_rate', 
          'is_group_member', 
          text = 'retention_rate', 
          percent = 'retention_rate', 
          position = 'dodge', 
          percent_deciamls = 0,
          facet = 'tier_type',
          nrow = 3) + 
theme(figure_size = (16, 10),
      legend_position='bottom') + 
labs(title="Cumulative Retention by Long Term  Status Lifetime Month",
     subtitle='By Tier Type',
     x = 'Lifetime Month')) 
