# Function to check for missing users
def get_missing_users(row):
    group_name = row['CompanyName'].upper()
    group_users = group_users_dict.get(group_name, set())
    company_users = set(row['Users'].upper().split(', '))
    missing_users = group_users - company_users
    return ', '.join(missing_users) if missing_users else None

# Apply the function to input2 dataframe to get missing users
input2_df['Missing_Users'] = input2_df.apply(get_missing_users, axis=1)

# If Missing_Users column is empty, set MissedCount to 0, otherwise count the missed users
input2_df['MissedCount'] = input2_df['Missing_Users'].apply(lambda x: 1 if pd.isna(x) else 0)
