comparison = df1.values != df2.values

# Get the row and column indices where differences occur
rows, cols = comparison.nonzero()

# Print differences
for row, col in zip(rows, cols):
    # Exclude the 'id' column which is not part of the comparison
    if df1.columns[col] != 'id':
        print(f"Row {row}, Column {df1.columns[col]}: df1 has {df1.iloc[row, col]}, df2 has {df2.iloc[row, col]}")
