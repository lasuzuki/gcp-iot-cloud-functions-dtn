import os
import io
import re
import json
import time
from google.cloud._helpers import _to_bytes
from google.cloud import pubsub_v1
from google.cloud import bigquery
subscriber = pubsub_v1.SubscriberClient()

# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(
  'your_project_id', 'your_subscription_id')
def callback(message):
  value = message.data  
  y = value.decode(encoding="utf-8")
  json_acceptable_string = y.replace("'", "\"")
  d = json.loads(json_acceptable_string)

  #Create a file with the sensing readings to be sent to host2 via bpsendfile
  with open('json.txt', 'w') as outfile:
    json.dump(d, outfile)

  #Persist the telemetry data on BigQuery
  client = bigquery.Client()
  dataset_ref = client.dataset('your_dataset')
  table_ref = dataset_ref.table('your_table')
  table = client.get_table(table_ref)
  
  errors = client.insert_rows_json(table,[d], row_ids=[None] * len(y))
  if not errors:
      print('Loaded in table')
  else:
      print('Errors:')
      for error in errors:
          print(error)
  
  #Send the json file to Host 2
  os.system(f'bpsendfile ipn:2.1 ipn:1.1 json.txt')
  
  #Acknowledge the receipt of the message to PubSub
  message.ack()
subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Currently listening for  messages on {}'.format(subscription_path))
while True:
  time.sleep(60)