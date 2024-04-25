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

# Function to process data and send notifications for applications ready for enablement
def process_data(table_a, table_b, room_id, token):
    for row in table_b.collect():
        org = row['ORG']
        app = row['Application']
        flag = row['Data Enabled Flag']
        # Filter table_a for the current application
        filtered_table_a = table_a.filter(table_a['Application'] == app).collect()
        # Check if filtered_table_a is not empty and flag is 'N'
        if filtered_table_a and flag == 'N':
            percentage_str = filtered_table_a[0]['Percentage']
            # Remove "%" sign and convert to integer
            status = int(percentage_str.replace("%", ""))
            if status == 100:
                send_webex_notification(room_id, f"Organization {org}: Application {app} is ready for enablement.", token)
            elif 90 <= status < 100:
                send_webex_notification(room_id, f"Organization {org}: Application {app} is upcoming for enablement.", token)

# Read tables from Databricks
table_a = spark.sql("SELECT * FROM table_a")
table_b = spark.sql("SELECT * FROM table_b")

# Specify Webex room ID and access token
webex_room_id = "your_room_id"
webex_token = "your_access_token"

# Process data and send notifications
process_data(table_a, table_b, webex_room_id, webex_token)
