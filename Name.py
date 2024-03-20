import pandas as pd

# Read the input Excel file
df = pd.read_excel('input.xlsx')

# Function to convert sizes to gigabytes
def convert_to_gb(size, unit):
    if unit == 'KB':
        return size / (1024 * 1024)
    elif unit == 'M':
        return size / 1024
    elif unit == 'MB':
        return size / 1024
    elif unit == 'G':
        return size
    elif unit == 'K':
        return size / (1024 * 1024)
    else:
        return None

# Convert sizes to gigabytes and remove unit columns
df['Actual Size (GB)'] = df.apply(lambda row: convert_to_gb(row['Actual Size'], row['Actual Size Unit']), axis=1)
df['Disk Size (GB)'] = df.apply(lambda row: convert_to_gb(row['Disk Size'], row['Disk Size Unit']), axis=1)
df.drop(columns=['Actual Size', 'Actual Size Unit', 'Disk Size', 'Disk Size Unit'], inplace=True)

# Convert 'Table' values to uppercase
df['Table'] = df['Table'].str.upper()

# Save the modified DataFrame to a new Excel file
df.to_excel('output.xlsx', index=False)
