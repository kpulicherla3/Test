import pandas as pd

# Function to convert sizes to gigabytes
def convert_to_gb(size_str):
    size, unit = size_str[:-1], size_str[-1]
    if unit == 'K':
        return float(size) / (1024 * 1024)
    elif unit == 'M':
        return float(size) / 1024
    elif unit == 'G':
        return float(size)
    else:
        return None

# Read the dispersed text file
with open('output.txt', 'r') as file:
    lines = file.readlines()

# Process lines and create a list of dictionaries
data = []
for line in lines:
    last_space_index = line.rfind(' ')
    sizes = line[:last_space_index].strip()
    file_name = line[last_space_index+1:].strip()
    apparent_size, disk_usage_size = sizes.split()
    apparent_size_gb = convert_to_gb(apparent_size)
    disk_usage_size_gb = convert_to_gb(disk_usage_size)
    data.append({'Apparent Size (GB)': apparent_size_gb, 'Disk Usage Size (GB)': disk_usage_size_gb, 'File': file_name})

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel
df.to_excel('output.xlsx', index=False)
