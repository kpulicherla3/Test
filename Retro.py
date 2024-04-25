import requests

# Function to send Webex notification
def send_webex_notification(room_id, message, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": room_id,
        "markdown": message
    }
    response = requests.post("https://webexapis.com/v1/messages", headers=headers, json=payload)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification. Status code:", response.status_code)

# Function to process data and print data enablement percentage
def process_data(table_a, table_b, room_id, token):
    org_data = {}
    for row in table_b.collect():
        org = row['ORG']
        app = row['Application']
        flag = row['Data Enabled Flag']
        status = table_a.filter(table_a['Application'] == app).collect()[0]['Percentage']
        if flag in ['N', 'Y']:
            if org not in org_data:
                org_data[org] = {'total_apps': 0, 'enabled_apps': 0, 'upcoming_apps': []}
            org_data[org]['total_apps'] += 1
            if flag == 'Y':
                org_data[org]['enabled_apps'] += 1
            elif 90 <= status < 100:
                org_data[org]['upcoming_apps'].append(app)
            if flag == 'N' and status == 100:
                send_webex_notification(room_id, f"Organization {org}: Application {app} is ready for enablement.", token)
            elif flag == 'N' and 90 <= status < 100:
                send_webex_notification(room_id, f"Organization {org}: Application {app} is upcoming for enablement.", token)
    
    # Calculate and print organization-wise data enablement percentage
    for org, data in org_data.items():
        if data['total_apps'] > 0:
            org_percentage = (data['enabled_apps'] / data['total_apps']) * 100
            print(f"Organization {org} - Data Enablement Percentage: {org_percentage}%")
            if data['upcoming_apps']:
                print(f"Organization {org}: Applications upcoming for enablement: {', '.join(data['upcoming_apps'])}")

# Read tables from Databricks
table_a = spark.sql("SELECT * FROM table_a")
table_b = spark.sql("SELECT * FROM table_b")

# Specify Webex room ID and access token
webex_room_id = "your_room_id"
webex_token = "your_access_token"

# Process data and send notifications
process_data(table_a, table_b, webex_room_id, webex_token)
