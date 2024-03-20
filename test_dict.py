test_output = {} 
tests   = ['t-test'] #, 'anova'] 
periods = ['cumulative', 'prior']
# groups  = ['tier_type', 'payment_provider']

test_output_dict = {'test': [],
                     'agg': []} 

t_test_dict_periods = {'cumulative': test_output_dict,
                       'prior':      test_output_dict}

anova_dict_periods  = {'cumulative':  [{'tier_type':        test_output_dict},
                                      {'payment_provider': test_output_dict}],
                       'prior':       [{'tier_type':        test_output_dict},
                                      {'payment_provider': test_output_dict}]}

for test in tests: 
    if test == 't-test': 
        test_output[test] = t_test_dict_periods
    elif test == 'anova': 
            test_output[test] = anova_dict_periods

test_output


{'t-test': {'cumulative': {'test': [], 'agg': []},
            'prior':      {'test': [], 'agg': []}},
 'anova': {'cumulative': [{'tier_type':        {'test': [], 'agg': []}},
                          {'payment_provider': {'test': [], 'agg': []}}],
            'prior':     [{'tier_type':        {'test': [], 'agg': []}},
                          {'payment_provider': {'test': [], 'agg': []}}]}}


IDs = [x for x in range(0,6)] 
Defaults = {'test': '', 'period': '', 'groups': '', 'stats': pd.DataFrame(), 'agg': pd.DataFrame()} # pd.DataFrame() 
test_output = dict.fromkeys(IDs, Defaults) 
test_output 



tests   = ['t-test'] #, 'anova'] 
periods = ['cumulative', 'prior']
# groups  = ['tier_type', 'payment_provider']

i = 0
for period in periods:
    i = i + 1
    print(i)
    for test in tests: 
        if test == 't-test':  
            if period == 'cumulative': 
                D[i]['test'] = test 
                D[i]['period'] = period 
                output, output2 = test_runner(new_subs_user_level, 
                                              test   = test,        
                                              metric = 'is_retained', 
                                              period = period, 
                                              groups = ['is_longterm_ucg']) 
                D[i]['stats'] = output
                D[i]['agg'] = output2

            # if period == 'prior': 
            #     print(test), print(period)
            #     test_output[test][period]['test'], test_output[test][period]['agg'] = test_runner(new_subs_user_level, 
            #                                                                                         test   = test,       
            #                                                                                         metric = 'is_retained', 
            #                                                                                         period = period,  
            #                                                                                         groups = ['is_longterm_ucg'])                 
        # elif test == 'anova': 
        #     break 
                # for group in groups: 
                # and group == 'is_longterm_ucg': 

test_output


for period in periods: 
    if period == 'cumulative': 
        cumulative_t_test = test_output['t-test']['cumulative']['test']
    elif period == 'prior': 
        prior_t_test = test_output['t-test']['prior']['test']

cumulative_t_test        











