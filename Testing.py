differences = []

# Iterate over columns
for col in df1.columns:
    if col in df2.columns:
        # Iterate over rows
        for i in range(len(df1)):
            if df1.at[i, col] != df2.at[i, col]:
                differences.append({
                    'Row': i,
                    'Column': col,
                    'df1 Value': df1.at[i, col],
                    'df2 Value': df2.at[i, col]
                })

# Create a DataFrame from the differences
differences_df = pd.DataFrame(differences)

# Display the differences
display(differences_df)  # Use Databricks'
