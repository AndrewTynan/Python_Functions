
# old example data 

# example data
np.random.seed(42)  

date_range = pd.date_range(start="2022-01-01", end="2023-12-01", freq="MS")  

df = pd.DataFrame({"year_month": date_range.strftime("%Y-%m"),  
                   "churn_rate": np.random.uniform(0.01, 0.20, len(date_range)),
                   "group_member": np.random.choice(["Group A", "Group B", "Group C"], len(date_range)) })

print(df.head())



# another old example data 

# Generate the date range
date_range = pd.date_range(start="2022-01-01", end="2023-12-01", freq="MS")

# Create the base DataFrame with year_month and group_member
base_df = pd.DataFrame({
    "year_month": date_range.strftime("%Y-%m"),
    "group_member": np.random.choice(["Group A", "Group B", "Group C"], len(date_range))
})

# Expand the DataFrame to include lifetime_month (1 to 12 for each cohort)
df = base_df.loc[base_df.index.repeat(12)].reset_index(drop=True)
df["lifetime_month"] = np.tile(range(1, 13), len(base_df))

# Generate a declining churn_rate for each row based on lifetime_month
# The churn_rate starts near 1.0 and declines as lifetime_month increases
df["churn_rate"] = 1.0 / (1 + np.exp((df["lifetime_month"] - 6) / 2))  # Sigmoid decay

# Show the result
df