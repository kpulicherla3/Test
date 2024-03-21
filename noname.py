import pandas as pd

# Read the CSV file
df = pd.read_csv('your_file.csv')

# Create a dictionary to store users for each group
group_users = {}

# Create a dictionary to store organization for each user
user_org = {}

# Create a dictionary to store unique users for each organization
org_users = {}

# Iterate over each row to populate the dictionaries
for index, row in df.iterrows():
    users = row['Users'].split(', ')
    group_name = row['Group Name']
    group_users[group_name] = set(users)
    org_prefix = group_name.split('_')[1]  # Extracting the organization prefix
    org_users[org_prefix] = org_users.get(org_prefix, set()) | set(users)
    for user in users:
        user_org[user.strip()] = org_prefix

# Create a new column for missed users
df['Missed Users'] = ''

# Iterate over each row to compute missed users
for index, row in df.iterrows():
    missed_users = set()
    org_prefix = row['Group Name'].split('_')[1]  # Extracting the organization prefix
    for group, users in group_users.items():
        if group != row['Group Name']:
            missed_users.update(users)
    missed_users -= set(row['Users'].split(', '))
    # Filter out missed users from different organizations
    missed_users = [user for user in missed_users if user_org.get(user, '') == org_prefix]
    df.at[index, 'Missed Users'] = ', '.join(missed_users)

# Save the updated DataFrame to a new CSV file
df.to_csv('output_file.csv', index=False)

print("Output saved to 'output_file.csv'.")

