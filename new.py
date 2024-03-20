with open('manager_emails.csv', 'w', newline='') as csvfile:
    fieldnames = ['Manager', 'Email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for manager, info in manager_info.items():
        writer.writerow({'Manager': manager, 'Email': info['email']})
