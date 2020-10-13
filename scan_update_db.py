import os
import time
from private import conf
# Below package needed to access Google Sheet
# How to get Google Credential: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
#pip install --upgrade oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
creds = ServiceAccountCredentials.from_json_keyfile_name(conf.client_secret_CarloAcutis1, scope)
client = gspread.authorize(creds)
sheet_device_monitoring = client.open("DeviceMonitoring").sheet1

row_of_devices = sheet_device_monitoring.row_values(1)
row_of_location = sheet_device_monitoring.row_values(2)
row_count = len(sheet_device_monitoring.col_values(1))
time_of_issue_repetition = list()
for device_ip in row_of_devices:
    time_of_issue_repetition.append(0)

for i in range(0, 100, 1):
    response_time = list()
    for device_order, device_ip in enumerate(row_of_devices):
        start_time = time.time()
        result = os.system("ping {} -c 1 > ./temp/ping_{}".format(device_ip, device_ip))
        # unreachable x=256, reachable x=0
        duration = time.time() - start_time
        if result == 256:
            time_of_issue_repetition[device_order] = time_of_issue_repetition[device_order] +1
            response_time.append("timeout")
            if time_of_issue_repetition[device_order] >= 3: os.system("say Network issue happen at location {}".format(row_of_location[device_order]))
        else:
            time_of_issue_repetition[device_order] = 0
            response_time.append(duration)
        print("==={}==={}".format(device_ip, duration))
    row_count = row_count + 1
    sheet_device_monitoring.append_row(response_time)
    if row_count > 102:
        while row_count > 102:
            sheet_device_monitoring.delete_rows(3, 3)
            sheet_device_monitoring.insert_row([], 104)
            row_count = row_count - 1
    time.sleep(3)


# x = os.system("ping 192.168.1.2 -c 1 | awk '{split($0, arr,\"/\"); print arr[5]}'")