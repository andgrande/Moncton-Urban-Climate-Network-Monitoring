library(lubridate)
library(xlsx)

file <- read.csv("C:/Users/anderson.grande/Documents/py/lesDates/2023_2024 Walmart Dieppe.csv", header = FALSE)
dates <- file[,2]
temps <- file[,3]

len <- length(dates)
dates_formatted <- parse_date_time(dates[3:len], orders = "%m/%d/%y  %H:%M:%S %p")

years <- year(dates_formatted)
months <- month(dates_formatted)
days <- day(dates_formatted)
week_days <- wday(dates_formatted, label = TRUE, abbr = FALSE)
hours <- hour(dates_formatted)
minutes <- minute(dates_formatted)
temps_trimmed <- temps[3:len]

data_to_excel <- data.frame(YEAR = years, MONTH = months, DAY = days, WEEK_DAY = week_days, HOUR = hours, MINNUTE = minutes, TEMPS = temps_trimmed)
write.xlsx(data_to_excel, file = "geisagrafia.xlsx", sheetName = "sheet_name")