def check_len(month):
    year = '2022'
    months = {"0" + str(month) if len(str(month)) < 2 else str(month) for month in range(1, 13)}
    three_months = {"04", "06", "09", "11"}
    three_one_months = months - three_months - {"02"}
    month = "0" + str(month) if len(str(month)) < 2 else str(month)
    if month in months and month in three_one_months:
        return 31
    if month in months and month in three_months:
        return 30
    if month == "02":
        if int(year) % 4 == 0:
            return 29
        else:
            return 28