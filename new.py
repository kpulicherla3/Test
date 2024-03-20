# Dictionary to store information for each manager
manager_info = defaultdict(lambda: {'users': set(), 'schemas': set(), 'applications': defaultdict(lambda: defaultdict(int)),
                                     'applications_used': set(), 'email': ''})  # Include 'email' key

# Iterate through each row to collect information
for row in data:
    manager = row['manager']
    user = row['user']
    schema = row['schema']
    application = row['app_name']
    email = row['email']  # Get manager's email

    # Exclude 'SCRATCH' and 'PROBABLE_SCRATCH' applications
    if application in {'SCRATCH', 'PROBABLE_SCRATCH'}:
        manager_info[manager]['applications']['Other'][schema] += 1
        continue

    # Count number of users for each manager
    manager_info[manager]['users'].add(user)

    # Count number of schemas for each manager
    manager_info[manager]['schemas'].add(schema)

    # Count number of occurrences of each application's schema
    if application:  # Only count if application is not null
        manager_info[manager]['applications'][application][schema] += 1
        manager_info[manager]['applications_used'].add(application)

    # Set manager's email
    manager_info[manager]['email'] = email

# Generate report for each manager
for manager, info in manager_info.items():
    email = info['email']  # Get manager's email

    # Count number of users for each manager
    num_users = len(info['users'])

    # Write data
    ws_info.append(['Number of Users', num_users])
    ws_info['A4'].font = header_font
    ws_info['A4'].fill = grey_fill  # Apply grey fill to this cell

    # Write email
    ws_info.append(['Email', email])
    ws_info['A5'].font = header_font
    ws_info['A5'].fill = grey_fill  # Apply grey fill to this cell
