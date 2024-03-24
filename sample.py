import pandas as pd

# Read the input files
input1_file = "company_groups.xlsx"
input2_file = "input2.csv"

# Read input data
input1_df = pd.read_excel(input1_file)
input2_df = pd.read_csv(input2_file)

# Group users in Input 1 by company name
grouped_input1 = input1_df.groupby('GroupName').agg({'Users': 'first', 'UserCount': 'first'}).reset_index()

# Group users in Input 2 by company name
grouped_input2 = input2_df.groupby('CompanyName')['Users'].apply(list).reset_index()

# Dictionary to store missing users for each group
missing_users_dict = {}

# Iterate over grouped input 2 data
for index, row in grouped_input2.iterrows():
    company_name = row['CompanyName'].upper()  # Convert to uppercase for case-insensitive comparison
    company_users = set(row['Users'])
    
    # Iterate over grouped input 1 data
    for _, group_row in grouped_input1.iterrows():
        group_name = group_row['GroupName'].upper()  # Convert to uppercase for case-insensitive comparison
        group_users = set(group_row['Users'].split(', '))
        
        # Check if company name is in group name (ignoring case) and if all users for the company are present in the group
        if company_name in group_name and not company_users.issubset(group_users):
            missing_users = list(company_users - group_users)
            if group_name not in missing_users_dict:
                missing_users_dict[group_name] = []
            missing_users_dict[group_name].extend(missing_users)

# Add missing users column to input 1
input1_df['Missing_Users'] = input1_df['GroupName'].apply(lambda x: ', '.join(missing_users_dict.get(x.upper(), [])))
input1_df['MissedCount'] = input1_df['Missing_Users'].apply(lambda x: len(x.split(', ')))

# Write the updated input 1 data to a new Excel file
output_file = "output.xlsx"
input1_df.to_excel(output_file, index=False)

print(f"Updated data has been written to {output_file}")
