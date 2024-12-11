
def facet(plot, facet_col, facet_scales=None, nrow=1): 

    if facet_scales is not None: # NOTE scales : Literal["fixed", "free", "free_x", "free_y"] = "fixed" 
        plt = (plot + facet_wrap(facet_col, nrow=nrow, scales=facet_scales))  
    else: 
        plt = (plot + facet_wrap(facet_col, nrow=nrow)) 

    return plt 


def col_plot(df, x, y, fill, **kwargs):  

    # kwargs options: 'position', 'facet', 'text', or 'percent' 

    max_val     = df.agg(max = (y, 'max')).iloc[0,0]
    max_val_pad = max_val + (max_val * 0.1)
    text_size = kwargs.get('text_size', 10)
    percent_deciamls = kwargs.get('percent_deciamls', 2)
    nudge_y = kwargs.get('nudge_y', 0)   
    
    if percent_deciamls == 1:
        deciamls = "{:.1f}%" 
    elif percent_deciamls == 0:
        deciamls = "{:.0f}%"        
    
    if 'position' in kwargs: 
        position = kwargs.get('position') 
    else:  
        position = 'stack' 

    plt = (ggplot(df) + 
            geom_col(position=position) + 
            aes(x = x, y = y, fill = fill))
    
    if 'facet' in kwargs:
        plt = facet(plt, 
                    facet_col = kwargs.get('facet'),
                    facet_scales = kwargs.get('facet_scales', 'fixed'), 
                    nrow = kwargs.get('nrow', 1))  

    if 'text' in kwargs and 'percent' in kwargs and position == 'dodge': # 'position' in kwargs:
        text = kwargs.get('text')    
        plt = (plt + geom_text(aes(label = text), position = position_dodge(width = 1), size = text_size, va="bottom", format_string=deciamls) #, nudge_y = nudge_y) 
                   + scale_y_continuous(labels = lambda l: ["%d%%" % v for v in l],
                                        limits = [0, 100])) 
        
    if 'text' in kwargs and 'percent' in kwargs and position == 'stack':
        text = kwargs.get('text')    
        plt = (plt + geom_text(aes(label = text), position = position_stack(vjust = 0.5), size = text_size, va="bottom", format_string=deciamls, nudge_y = nudge_y) 
                   + scale_y_continuous(labels = lambda l: ["%d%%" % v for v in l],
                                        limits = [0, 100]))  
    
    if 'text' in kwargs and 'percent' not in kwargs:
        text = kwargs.get('text')    
        if 'position' in kwargs:
            position = kwargs.get('position') 
            if position == 'dodge': # NOTE default position = "stack", which might be useful sometimes.. 
                plt = (plt + geom_text(aes(label = text), position = position_dodge(width = 1), size = text_size, va="bottom", format_string="{:,}"))
        else: 
            plt = (plt + geom_text(aes(label = text), size = text_size, va="bottom", format_string="{:,}")) 
        
        plt = (plt + scale_y_continuous(labels = comma_format(),
                                        limits = [0, max_val_pad]))
        
    plt = (plt + labs(x=x.replace("_", " ").title(), 
                      y=y.replace("_", " ").title()) 
               + guides(fill = guide_legend(title = y.replace("_", " ").title())))   
    
    return plt 
