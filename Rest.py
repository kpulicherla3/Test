comparison = df1.iloc[:, 1:] != df2.iloc[:, 1:]

# Find the locations of the differences
rows, cols = comparison.stack()[comparison.stack()].index.tolist()

# Print differences
for row, col in zip(rows, cols):
    print(f"Row {row+1}, Column {df1.columns[col+1]}: df1 has {df1.iloc[row, col+1]}, df2 has {df2.iloc[row, col+1]}")
