
def facet(plot, facet_col, facet_scales=None, nrow=1): 

    if facet_scales is not None: # NOTE scales : Literal["fixed", "free", "free_x", "free_y"] = "fixed" 
        plt = (plot + facet_wrap(facet_col, nrow=nrow, scales=facet_scales))  
    else: 
        plt = (plot + facet_wrap(facet_col, nrow=nrow)) 

    return plt 
