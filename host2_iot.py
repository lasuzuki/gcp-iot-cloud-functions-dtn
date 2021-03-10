import os
import shutil
import json
import re
import os.path
import time
import io
from datetime import datetime
import requests
while True:

#path = os.path.abspath('testfile1'
  if os.path.exists("testfile1"):
     temperature = 0
     pressure = 0
     humidity = 0
     x = 0
     y = 0
     z = 0
     print("File Found")
     now = datetime.now()
     file_name = os.path.abspath('testfile1')
     with open(file_name, "r") as read_file:
       data = json.load(read_file)
       for key in data:
         ts = data['ts']
         temperature = data['temperature']
         pressure = data['pressure']
         humidity = data['humidity']
         x = data['x']
         y = data['y']
         z = data['z']
       pass
     #Do something with the telemetry data. In our case we use a very simple example using acceleration measurements
     if z > 1 or y > 1 or z > 1:
       #Send a HTTP request to the Cloud Function we Deployed  
       r =requests.get('https://us-central1-dtn-host-iot-297209.cloudfunctions.net/iot-cf?message=red')
       print(r.status_code)    
     #Move the processed file to a folder containing all the files received from Host 1
     name = "file" + str(int(datetime.timestamp(now)))
     os.rename('testfile1',name)
     path = "your_path/ion-open-source-4.0.0/dtn/processed/"
     shutil.move(name, path)
  else:
    print("Waiting for file via DTN")
    value = "bprecvfile ipn:1.1"
    os.system('bprecvfile ipn:1.1 1')
    if os.path.exists("testfile1"):
      print("File Received via DTN")
  time.sleep(10)
