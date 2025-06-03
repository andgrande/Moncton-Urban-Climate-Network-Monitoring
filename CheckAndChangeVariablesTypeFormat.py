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

df.rename(columns={'Unnamed: 0': 'Date', '\nTemperature': 'Temp_High', 'Unnamed: 2': 'Temp_Avg', 'Unnamed: 3': 'Temp_Low', 'Dew Point': 'DewPoint_High',
       'Unnamed: 5': 'DewPoint_Avg', 'Unnamed: 6': 'DewPoint_Low', 'Humidity': 'Humidity_High', 'Unnamed: 8': 'Humidity_Avg', 'Unnamed: 9': 'Humidity_Low', 'Speed': 'Speed_High',
       'Unnamed: 11': 'Speed_Avg', 'Unnamed: 12': 'Speed_Low', 'Pressure': 'Pressure_High', 'Unnamed: 14': 'Pressure_Low'}, inplace=True)

df = df.drop(index=0, axis=0)

# df.Temp_High.str.replace('°C', '', inplace=True).str.strip()
# df.Temp_High.astype(float)

df.replace({r'\s*°C': '', r'\s*km/h': '', r'\s*hPa': '', r'\s*mm': '', ',': '', r'\s*%': ''}, regex=True, inplace=True)

for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='raise')

print(df.info())

df.to_excel('Formatted_{}'.format(file_name), index=False)

print("")
print("The file has been formatted and saved as 'Formatted_{}'.".format(file_name))
time.sleep(5)
print("")