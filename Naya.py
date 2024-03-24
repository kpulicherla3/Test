group_users = set()
if isinstance(group_row['Users'], str) and group_row['Users']:
    group_users = set(group_row['Users'].split(', '))
