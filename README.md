# Moncton Urban Climate Network Monitoring

This is an ongoing project in which its content aims to aid and collaborate with the Université de Moncton "Urban Climate Monitoring Network for adaptation to climate change in the greater Moncton area (RESCUM) project", funded by the NBIF - Climate Impact Mitigation Fund.

Languages used: **Python** and **R**

- **CheckMissingDates.R** script handles the identification of data failures and organization of the weather data set from 1870 to 2024 for 159 weathe rstations in new Brunswick.
- **FormatDatesFromCsv.R** script helps to separate and format dates for better readability in Excel.
- **FileGenerationFromDataExtraction.py** script handles the Data extraction, cleaning and analysis on the hourly data from 10 weather stations located in the Great Moncton area, NB and deliver it in a csv file. - API Data source: www.wunderground.com
- **DataConsistencyReport.py** script handes the analysis of the confireliability of the extracted data.

Further tasks should provide data handling and graph visualization.

In order to run the **FileGenerationFromDataExtraction.py** script an API Key will be needed in order to connect with wunderground website. Rename the **template.env** file to **.env** and replace the API Key value there.


## License

MIT