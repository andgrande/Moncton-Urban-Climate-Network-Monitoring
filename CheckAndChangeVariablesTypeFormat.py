import time
import pandas as pd
import os

print(" ------------------------------------------------------------------------------------------------ ")
print("| Assurez-vous que le fichier de feuille de calcul est présent dans le même dossier que le script |")
print("| Make sure worksheet file is present in the same folder as the script                            |")
print(" ------------------------------------------------------------------------------------------------ ")

root_path = os.getcwd()
file_name = input('Type the name of the Excel file to be updated: ')

if not file_name.endswith('.xlsx'):
    file_name += '.xlsx'

excel_file = os.path.join(root_path, file_name)
df = pd.read_excel(excel_file)

# def rename_colums(df):
df.rename(columns={'Unnamed: 0': 'Date', '\nTemperature': 'Temp_High', 'Unnamed: 2': 'Temp_Avg', 'Unnamed: 3': 'Temp_Low', 'Dew Point': 'DewPoint_High',
    'Unnamed: 5': 'DewPoint_Avg', 'Unnamed: 6': 'DewPoint_Low', 'Humidity': 'Humidity_High', 'Unnamed: 8': 'Humidity_Avg', 'Unnamed: 9': 'Humidity_Low', 'Speed': 'Speed_High',
    'Unnamed: 11': 'Speed_Avg', 'Unnamed: 12': 'Speed_Low', 'Pressure': 'Pressure_High', 'Unnamed: 14': 'Pressure_Low'}, inplace=True)

df = df.drop(index=0, axis=0)

    # return df

# def remove_unecessary_characters(df):
df.replace({r'\s*°C': '', r'\s*km/h': '', r'\s*hPa': '', r'\s*mm': '', ',': '', r'\s*%': ''}, regex=True, inplace=True)
    # return df

# def fix_dataTypes(df):
df['Date'] = pd.to_datetime(df['Date'], errors='raise').dt.date
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='raise')

    # return df

# Instructions for setting a range, checking for missing dates, and formatting the DataFrame
start_date = df.Date.loc[1]
end_date = df.Date.loc[len(df.Date) - 1]
date_range = pd.date_range(start=start_date, end=end_date)

df_temp = pd.DataFrame(columns=['Date'])

missing_dates = []
my_counter = 0
for date in date_range:
    date_only = date.date()
    if date_only not in df['Date'].values:
        missing_dates.append({'Date': date_only})
        my_counter += 1

df_temp = pd.DataFrame(missing_dates)
df = pd.concat([df, df_temp], ignore_index=True)
df = df.sort_values(by='Date').reset_index(drop=True)

# Saving to Excel and Printing the results
print("")

df.to_excel('Formatted_{}'.format(file_name), index=False)

print("")
print("The file has been formatted and saved as 'Formatted_{}'.".format(file_name))
print("")

print("Whole date range size: ", date_range.size + 1)
print(my_counter, "missing dates found in the data.")
print("")

sair = input("Press any key to exit...")
# rename_colums(df)
# remove_unecessary_characters(df)
# fix_dataTypes(df)
# print_results(df)
