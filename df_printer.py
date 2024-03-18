
def df_printer(df): 
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(3,3), dpi=300)
    ax = plt.subplot()

    ncols = df.shape[1]
    nrows = df.shape[0] 
    columns = list(df.columns)

    positions = list()
    for i in range(0, ncols): 
        if i == 0:
            positions.append(0.25)
        else: 
            positions.append(i + 1.5) 

    ax.set_xlim(0, ncols + 1)
    ax.set_ylim(0, nrows)            

    # Add table's main text
    for i in range(nrows):
        for j, column in enumerate(columns):
            if j == 0:
                ha = 'left'
            else:
                ha = 'center'
            ax.annotate(
                xy=(positions[j], i),
                text=df[column].iloc[i],
                ha=ha,
                va='center',
                size=3)

    # Add column names
    columns_names = [x.replace("_", " ").title() for x in list(df.columns)]
    for index, c in enumerate(columns_names):
            if index == 0:
                ha = 'left'
            else:
                ha = 'center'
            ax.annotate(
                xy=(positions[index], nrows),
                text=columns_names[index],
                ha=ha,
                va='bottom',
                weight='bold',
                size=2.5)
    ax.set_axis_off()
    plt.show() 
