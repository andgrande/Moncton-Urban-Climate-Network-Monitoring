# Carregar bibliotecas necessárias
install.packages("dplyr")
install.packages("lubridate")
install.packages("readxl")
library(dplyr)
library(lubridate)
library(readxl)

print_results <- function(total_range, missing_dates, current_sheet,total_registered_dates,print_dates) {
  if (!length(missing_dates)) {
    print(paste("No missing dates in sheet", current_sheet))
  }
    print("------------------------------------------------------------")
    print(paste("RESULTS FOR SHEET",current_sheet))
    print(paste("OLDEST DATE REGISTERED IN THE INTERVAL: ",min(total_range)))
    print(paste("NEWEST DATE REGISTERED IN THE INTERVAL: ",max(total_range)))
    print(paste("OLDEST MISSING DATE: ",min(missing_dates)))
    print(paste("LATTER MISSING DATE: ",max(missing_dates)))
    print(paste("Total dates in the interval: ", length(total_range)))
    print(paste("Total missing dates in sheet: ", length(missing_dates)))
    if (print_dates == "y" | print_dates == "Y") print(missing_dates)
}

handle_data_verification <- function(current_sheet,excel_path_name,print_dates) {
  if (current_sheet != "Export Summary") {
    sheet_data <- read_excel(excel_path_name, sheet = current_sheet, .name_repair = ~make.unique(.x, sep = "_") )

    data_x_col <- sheet_data$'DATE'
    data_x_col_formatted <- as.POSIXlt(data_x_col, format = "%Y-%m-%d", tz = "UTC")
    total_registered_dates <- length(data_x_col)

    # IF SHEET CONTAINS DATES OLDER THAN THE 1900s
    if (anyNA(data_x_col_formatted)) {
      data_without_na <- data_x_col_formatted[-which(is.na(data_x_col_formatted))]
      lenIni <- length(data_without_na) + 1
      lenFin <- length(data_x_col_formatted)

      data_with_na <- data_x_col[lenIni:lenFin]

      # PRE-1900s SECTION
      if (data_x_col_formatted[1] < as.Date("1900-01-01")) {
        data_without_na_formatted <- as.POSIXct(data_without_na, format = "%Y-%m-%d", tz = "UTC")
        total_range <- seq(from = min(data_without_na), to = max(data_without_na), by = "day")
        missing_dates <- as.POSIXlt(setdiff(total_range, data_without_na_formatted), tz = "UTC")
        
        print_results(total_range, missing_dates,current_sheet,total_registered_dates,print_dates)
      }

      # POST-1900s SECTION
      data_with_na_integer <- as.numeric(data_with_na)
      data_with_na_formatted <- as.Date(data_with_na_integer, origin = "1899-12-30", format = "%Y-%m-%d")
      total_range <- seq(from = min(data_with_na_formatted), to = max(data_with_na_formatted), by = "day")
      missing_dates <- as.Date(setdiff(total_range, data_with_na_formatted), tz = "UTC")

      print_results(total_range, missing_dates,current_sheet,total_registered_dates, print_dates)

    } else { # IF NO DATES PRIOR TO 1900s WERE FOUND
      total_range <- seq(from = min(data_x_col), to = max(data_x_col), by = "day")
      missing_dates <- as.POSIXlt(setdiff(total_range, data_x_col), tz = "UTC")
      missing_dates_formatted <- format(missing_dates,"%Y-%m-%d")

      print_results(total_range, missing_dates,current_sheet,total_registered_dates, print_dates)
    }
  }
}

main <- function() {
  # Necessário informar a base de dados a ser lida, no caso um documento Excel
  path_name <- readline(prompt = "Copy and paste here the location folder where the excel is (Ex: C:/Users/.../): ")
  excel_name <- readline(prompt = "Inform the excel name (Ex: Moncton): ")
  print_dates <- readline(prompt = "Print missing dates? (y/n): ")
  setwd(path_name)
  excel_path_name <- paste(getwd(),"/",excel_name,".xlsx", sep = "")
  sheets_list <- excel_sheets(excel_path_name)

  for (current_sheet in sheets_list) {
    handle_data_verification(current_sheet, excel_path_name, print_dates)
  }
}

main()