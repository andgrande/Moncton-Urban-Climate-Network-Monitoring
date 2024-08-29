import pandas as pd

range_list = pd.to_datetime(pd.date_range('20230101', '20240818', freq='1h')).strftime("%d-%m-%Y %H")
df1 = pd.DataFrame({'date': range_list})
df1 = df1.drop(df1.index[-7:])

def iterate_stations(range_list):
    station_list = ['IDIEPP3', 'IDIEPP11', 'IRIVER76', 'IRIVER4', 'IRIVER28', 'IMONCT37', 'IMONCT20', 'INEWBRUN43', 'IMONCT23', 'IMONCT38']
    station_list.sort()
    data = pd.read_csv(r"GMA-ALL_20230101-20240817.csv")

    expected_total_counts = 0
    actual_total_counts = 0
    missing_dates_dict = dict()


    for station in station_list:
        print('"{}": \n'.format(station))
        data_filtered = data[data['stationID'] == station]

        date = pd.to_datetime(data_filtered['obsTimeLocal']).dt.strftime("%d-%m-%Y %H")
        df2 = pd.DataFrame({'date': date})

        merged = df1.merge(df2, on='date', how='left', indicator=True)
        registros_faltantes = str(len(df1) - len(df2))
        porcentagem_registros_faltantes = str(round(100 - len(df2) * 100 / len(df1), 2))
        print("Registros esperados: " + str(len(df1)))
        print("Registros faltantes: {} = {}%".format(registros_faltantes, porcentagem_registros_faltantes))
        print("-------------------------------")

        expected_total_counts += len(df1)
        actual_total_counts += len(df2)
        
        lefted_merge = merged[merged['_merge'] == 'left_only']
        if station == 'IRIVER4':
        # print(df1)
            print(lefted_merge)
            merged.to_csv("Test.csv", index = False)

    print("\nTotal esperado: " + str(expected_total_counts))
    print("Total coletado: " + str(actual_total_counts) + " = " + str(round(actual_total_counts * 100 / expected_total_counts, 2)) + "%")

iterate_stations(range_list)
