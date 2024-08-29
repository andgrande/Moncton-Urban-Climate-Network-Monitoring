import os
from dotenv import load_dotenv
import requests
import json
import csv
import datetime
import pandas as pd

load_dotenv()

api_key = os.getenv('API_KEY')
if api_key is None: 
     api_key = input("Input your API KEY: ")

data_type = 'hourly' # can be 'daily', 'hourly', or 'all'
default_input_date = "20230101"
station_list = ['IDIEPP3', 'IDIEPP11', 'IRIVER76', 'IRIVER4', 'IRIVER28']
# station_list = ['IMONCT37', 'IMONCT20', 'INEWBRUN43', 'IMONCT23', 'IMONCT38']
counter = { 
     'header_counter': 0, 
     'incomplete_data': {
          'date-incomplete': 'available_amount'
     },
     'failure_at': []
}

print('\nEnter start date for the extraction: (ENTER for "2023-01-01")')
input_date = input().format('%Y%m%d')
if input_date:
     date_start_date = input_date.replace("-","")
else: date_start_date = default_input_date
date_end_date = datetime.datetime.now().strftime('%Y%m%d')
date_range_list = pd.date_range(date_start_date, date_end_date).strftime('%Y%m%d').tolist()

file_name = '{station}_{start_date}-{end_date}.csv'.format(station = "GMA", start_date = date_start_date, end_date = date_end_date)

# LOCAL TESTING CODE - without calling the API
#
# file = open(file_name, mode='w', newline='')
# csv_writer = csv.writer(file)

def handle_csv_creation(json_data, csv_writer, api_date):
     observations = json_data['observations']

     if len(observations) < 24:
         counter['incomplete_data'][api_date] = len(observations)

     for row in observations:
          metric_tag = row['metric']
          row.update(metric_tag)
          row.pop('metric')
          
          if counter['header_counter'] == 0:
               header = row.keys()
               csv_writer.writerow(header)
               counter.update({'header_counter': counter['header_counter'] + 1})
               
          csv_writer.writerow(row.values())

datasheet_values = []
def handle_populate_datasheet(json_data):
     observations = json_data['observations']
     if len(observations) < 24:
         counter['incomplete_data'][api_date] = len(observations)

     for row in observations:
          metric_tag = row['metric']
          row.update(metric_tag)
          row.pop('metric')

          datasheet_values.append(row)

failure_counter = 0
for api_date in date_range_list:
     for station in station_list:
          if failure_counter > len(station_list): break
          try:
               response = requests.get("https://api.weather.com/v2/pws/history/{data_type}?stationId={station}&format=json&units=m&date={api_date}&apiKey={api_key}".format(data_type = data_type, station = station, api_date = api_date))
               json_data = response.json()
               handle_populate_datasheet(json_data)
               print("Handled {} at {}".format(station, api_date))
          except: 
               # Need to enhance error handling
               break

# LOCAL TESTING CODE - without calling the API
#
# with open(r"C:\Users\anderson.grande\Documents\py\wu\data.json") as json_file:
# 	data = json.load(json_file)    
#    handle_csv_creation(data, csv_writer, api_date = '20230103')
# file.close()

df = pd.DataFrame(datasheet_values)
df.to_csv('{}'.format(file_name), index=False)

print('\nFile "{}" created.\n'.format(file_name))
print(counter)
print(len(datasheet_values))