import pandas as pd
from webexteamssdk import WebexTeamsAPI
import subprocess

# Function to execute shell command
def execute_shell_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8')
    return result.stdout

# Function to generate group names based on companies
def generate_group_names(companies):
    group_names = []
    for company in companies:
        group_names.extend([f"managers_{company}", f"nonit_{company}", f"it_{company}"])
    return group_names

# Function to process groups and return data as a dictionary
def process_groups(group_names):
    groups_data = {}
    for group_name in group_names:
        output = execute_shell_command(f"net group {group_name} /domain")

        # Split the output by lines and extract users starting from line 7
        lines = output.splitlines()
        users = []

        for line in lines[7:]:
            if line.strip().startswith('The command completed successfully.'):
                break
            if line.strip():
                # Split each line by spaces to extract users
                line_users = line.strip().split()
                # Add the users to the main list
                users.extend(line_users)
        groups_data[group_name] = {
            "Users": users,
            "Number of Users": len(users)
        }

    return groups_data

# Main function
def main():
    companies = ["apple", "cisco", "nvidia"]  # List of companies
    group_names = generate_group_names(companies)
    groups_data = process_groups(group_names)

    # Convert groups_data dictionary to DataFrame
    df = pd.DataFrame(groups_data).T.reset_index()
    df.columns = ['Group Name', 'Users', 'Number of Users']

    return df

if __name__ == "__main__":
    df = main()  # Get DataFrame from the first script
    csv_data = pd.read_csv("input2.csv")  # Load data from CSV file

    # Function to find missed users for each group
    def find_missed_users(group_name, company_name):
        # Get users for the given group and company
        group_users = df.loc[df['Group Name'].str.contains(group_name, case=False), 'Users'].iloc[0]
        if pd.isna(group_users):
            group_users_list = []
        else:
            group_users_list = [user.strip().lower() for user in group_users.split(',')]
        
        # Get critical users for the company
        company_users = csv_data.loc[csv_data['CompanyName'].str.upper() == company_name.upper(), 'Users'].tolist()
        
        # Find missed users
        missed_users = [user for user in company_users if user.lower() not in group_users_list]
        return missed_users, len(missed_users)

    # Add a new column to DataFrame to store the corresponding company name
    df['CompanyName'] = ""

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        group_name = row['Group Name'].upper()
        # Check if any company name from the CSV file matches the group name
        for company_name in csv_data['CompanyName']:
            if company_name.upper() in group_name:
                # Assign the matching company name to the new column
                df.at[index, 'CompanyName'] = company_name.upper()
                break  # Move to the next row in the DataFrame

    # Add columns for missed users and missed users count
    df['MissedUsers'] = ""
    df['MissedUsersCount'] = ""

    # Iterate through each row in the DataFrame to find missed users
    for index, row in df.iterrows():
        missed_users, missed_users_count = find_missed_users(row['Group Name'], row['CompanyName'])
        df.at[index, 'MissedUsers'] = ', '.join(missed_users)
        df.at[index, 'MissedUsersCount'] = missed_users_count

    # Save the modified DataFrame to a CSV file
    df.to_csv("output.csv", index=False)

    # Send Webex notification with the CSV file attached
    api = WebexTeamsAPI("YOUR_ACCESS_TOKEN")
    message = "Here is the output CSV file."
    room_id = "YOUR_ROOM_ID"
    file_path = "output.csv"

    api.messages.create(roomId=room_id, text=message, files=[file_path])
