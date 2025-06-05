import os
# from dotenv import load_dotenv
import requests
import json
import csv
import datetime
import pandas as pd

# load_dotenv()

# api_key = os.getenv('API_KEY')
# if api_key is None: 
#      api_key = input("Input your API KEY: ")

api_key = "096ef67eabe14c8daef67eabe1cc8d05"
print()
# data_type = 'hourly' # can be 'daily', 'hourly', or 'all'
data_type_option = input("Choose frequency of observations. Press 1 for 'Hourly' or 2 for 'Daily': ")
data_type = 'hourly' if data_type_option == '1' else 'daily'

default_start_date = "20230101"
default_end_date = "20250531"
# station_list = ['IDIEPP3', 'IDIEPP11', 'IRIVER76', 'IRIVER4', 'IRIVER28', 'IMONCT37', 'IMONCT20', 'INEWBRUN43', 'IMONCT23', 'IMONCT38']
stations = input("Input the stations (comma separated), like 'IDIEPP11, IRIVER76, IMONCT20': ")

stations_trimmed = stations.replace('"', '').replace("'", "")

station_list = [station.strip() for station in stations_trimmed.split(',') if station.strip()]

counter = { 
     'header_counter': 0, 
     'incomplete_data': {
          'date-incomplete': 'available_amount'
     },
     'failure_at': []
}

print('\nEnter START DATE (YYYMMDD) for the extraction: (Press ENTER for "2023-01-01")')
input_date = input().format('%Y%m%d')
if input_date:
     date_start_date = input_date.replace("-","")
else: date_start_date = default_start_date

print('\nEnter LAST DATE (YYYMMDD) for the extraction: (Press ENTER for "2025-05-31")')
input_date = input().format('%Y%m%d')
if input_date:
     date_end_date = input_date.replace("-","")
else: date_end_date = default_end_date

# date_end_date = datetime.datetime.now().strftime('%Y%m%d')
date_range_list = pd.date_range(date_start_date, date_end_date).strftime('%Y%m%d').tolist()

file_name = '{station}_{start_date}-{end_date}.csv'.format(station = "GMA", start_date = date_start_date, end_date = date_end_date)
print()
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

# LOCAL TESTING CODE - without calling the API
#
def local_testing():
     main_data = {}
     with open(r"C:\Users\anderson.grande\Documents\py\Ge\wu\tempDelete\hourly.json") as json_file:
          main_data = json.load(json_file)
          # handle_csv_creation(data, csv_writer, api_date = '20230103')
          return main_data
     json_file.close()

datasheet_values = []
def handle_populate_datasheet(json_data):
     observations = json_data['observations']
     # print(len(observations))
     # if len(observations) < 24:
     #     counter['incomplete_data'][api_date] = len(observations)

     for row in observations:
          metric_tag = row['metric']
          row.update(metric_tag)
          row.pop('metric')

          datasheet_values.append(row)

# failure_counter = 0
for api_date in date_range_list:
     for station in station_list:
          # if failure_counter > len(station_list): break
          try:
               # uncomment the next two lines to use the API
               response = requests.get("https://api.weather.com/v2/pws/history/{data_type}?stationId={station}&format=json&units=m&date={api_date}&numericPrecision=decimal&apiKey={api_key}".format(data_type = data_type, station = station, api_date = api_date, api_key = api_key))
               json_data = response.json()
               # json_data = local_testing()  # Use this line for local testing
               handle_populate_datasheet(json_data)
               print("Handled {} at {}".format(station, api_date))
          except: 
               # Need to enhance error handling
               break



df = pd.DataFrame(datasheet_values)


df.insert(4, 'hour', df.obsTimeLocal.astype('datetime64[ns]').dt.hour)  # Extract hour from obsTimeLocal'])
# df['hour'] = df.obsTimeLocal.astype('datetime64[ns]').dt.hour
df['bdate'] = df.obsTimeLocal.astype('datetime64[ns]').dt.date

date_range_list = pd.date_range(date_start_date, date_end_date).strftime('%Y-%m-%d').tolist()
date_range_list = pd.to_datetime(date_range_list, format='%Y-%m-%d').date.tolist()
hours_range_list = range(0, 24)

def fix_missing_dates(df, date_range_list, station_list):
     for date in date_range_list:
          for station in station_list:
               for hour in hours_range_list:
                    dft = df[(df['stationID'] == station) & (df['bdate'] == date) & (df['hour'] == hour)]
                    # if not df[(df['stationID'] == station) & (df['bdate'] == date) & (df['hour'] == hour)].empty:
                    if dft.empty:
                         dftd = datetime.datetime.combine(date, datetime.time(hour, 0))
                         # add line to the df
                         dfTemp = pd.DataFrame({'stationID': [station], 'obsTimeLocal': [dftd], 'hour': [hour]})
                         # df.loc[len(df)] = [station, dftd, None, None, hour, date]
                         df = pd.concat([df, dfTemp], ignore_index=True)
                         # print("NAO EXISTE ", hour)
     return df

if data_type == 'hourly':
     df = fix_missing_dates(df, date_range_list, station_list)

df['obsTimeLocal'] = pd.to_datetime(df['obsTimeLocal'])

# This is broken
df = df.sort_values(by=['stationID', 'obsTimeLocal']).reset_index(drop=True)

# for api_date in date_range_list:
#      for station in station_list:
#           # if data_type == 'hourly':
#           df[df['obsTimeLocal'].str.startswith(api_date)] = station

df.to_csv('{}'.format(file_name), index=False)

print('\nNew file "{}" created.\n'.format(file_name))
# print(counter)
# print(len(datasheet_values))

sair = input("Press any key to exit...")
