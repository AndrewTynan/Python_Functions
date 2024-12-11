
def tabyl_two_vars(df, var1, var2, percents="No"):

    var_names = var1 + " / " + var2

    if percents == "No":
        df = df.groupby([var1, var2]).size().reset_index().rename({0: "n"}, axis=1)

        df = (pd.pivot_table(df, values="n", index=[var1], columns=var2)
              .reset_index()
              .rename_axis(None, axis=1))
        df = df.rename({var1: var_names}, axis=1)
        df = df.style.hide() 

    elif percents == "Yes":
        df = df.groupby([var1, var2]).size().reset_index().rename({0: "n"}, axis=1)

        df = pd.crosstab(df[var1], df[var2], normalize="index").reset_index() # index, 'all', 'columns'
        df.columns.name = ''
        df = df.rename(columns={df.columns[0]: var_names})         

    return display(ip.display.HTML(df.to_html())) 

# examples 
# tabyl_two_vars(monthly_mex_food_df, "food", "months")
# tabyl_two_vars(monthly_mex_food_df, "food", "months", percents="Yes")

tabyl_two_vars(points_df, "league", "points_bucket")


print('can also chose to report percents')
tabyl_two_vars(points_df, "league", "points_bucket", percents="Yes")