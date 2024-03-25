import subprocess
import pandas as pd

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

    print(df)

if __name__ == "__main__":
    main()
