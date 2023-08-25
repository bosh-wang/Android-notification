import requests
import time
import datetime
import pytz
from keep_alive import keep_alive
import json

keep_alive()

print("Notification service starts at",
      datetime.datetime.now(pytz.timezone('Asia/Taipei')).strftime("%H:%M:%S"))


def process_data(current_time, drug_name, token):
  return {
    "to":f"{token}",
    "notification": {
      "title": "小護士提醒您 該吃藥囉",
      "body": f"現在時間{current_time} 要吃 {drug_name}"
    }
  }


notification_url = "https://fcm.googleapis.com/fcm/send"

todayReminder_url = "https://medicinehelper.pythonanywhere.com/todayReminders"

notification_headers = {
  "Content-Type":
  "application/json",
  "Authorization":
  "key=key"
}

while True:

  todayReminder_response = requests.get(todayReminder_url)
  todayReminder_info = todayReminder_response.json()

  f = open("token.json")
  tokens = json.load(f)['id']
  

  current_time = datetime.datetime.now(
    pytz.timezone('Asia/Taipei')).strftime("%H:%M")

  for i in range(len(todayReminder_info)):
    drug_info = todayReminder_info[i]
    drug_timeSlot = drug_info['timeSlot']
    if current_time == drug_timeSlot:
      drug_name = drug_info['drug']['name']

      for i in range(len(tokens)):
      
        notification_data = process_data(current_time, drug_name, tokens[i])
        
        notification_response = requests.post(notification_url,
                                              json=notification_data,
                                              headers=notification_headers)
  
        print(f"successfully send notification at {current_time} to token {tokens[i]}"
              if notification_response.json()['success'] ==
              1 else f"failed to send notification at {current_time}")

  time.sleep(59)
