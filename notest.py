import pandas as pd

# Load data from Excel file
excel_data = pd.read_excel("company_groups.xlsx")

# Load data from CSV file
csv_data = pd.read_csv("input2.csv")


# Function to find missed users for each group
def find_missed_users(group_name, company_name):
    # Get users for the given group and company
    group_users = excel_data.loc[excel_data['GroupName'].str.contains(group_name, case=False) & 
                                  (excel_data['CompanyName'] == company_name.upper()), 'Users'].iloc[0]
    if pd.isna(group_users):
        group_users_list = []
    else:
        group_users_list = [user.strip().lower() for user in group_users.split(',')]
    
    # Get critical users for the company
    company_users = csv_data.loc[csv_data['CompanyName'].str.upper() == company_name.upper(), 'Users'].tolist()
    
    # Find missed users
    missed_users = [user for user in company_users if user.lower() not in group_users_list]
    return missed_users, len(missed_users)

# Add a new column to Excel data to store the corresponding company name
excel_data['CompanyName'] = ""

# Iterate through each row in the Excel file
for index, row in excel_data.iterrows():
    group_name = row['GroupName'].upper()
    # Check if any company name from the CSV file matches the group name
    for company_name in csv_data['CompanyName']:
        if company_name.upper() in group_name:
            # Assign the matching company name to the new column
            excel_data.at[index, 'CompanyName'] = company_name.upper()
            break  # Move to the next row in the Excel file

# Add columns for missed users and missed users count
excel_data['MissedUsers'] = ""
excel_data['MissedUsersCount'] = ""

# Iterate through each row in the Excel file to find missed users
for index, row in excel_data.iterrows():
    missed_users, missed_users_count = find_missed_users(row['GroupName'], row['CompanyName'])
    excel_data.at[index, 'MissedUsers'] = ', '.join(missed_users)
    excel_data.at[index, 'MissedUsersCount'] = missed_users_count

# Save the modified Excel file
excel_data.to_excel("output.xlsx", index=False)
