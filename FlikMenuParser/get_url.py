import parsing as ps
from month_length import check_len

# day_url funcion will return a url in the format of a string
def day_url(date, meta):
    prefix, school_id, menu_type, year = meta["prefix"], meta["school_id"], meta["menu_type"], meta["year"]
    month, day = date[0], date[1]
    url = rf"https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}"
    return url

# url_list will generate a list of urls with a range of dates, NOTE: date1 and date2 must be each given in a list [MM,DD]
"""
def url_list(date1, date2, meta):
    prefix, school_id, menu_type, year = meta["prefix"], meta["school_id"], meta["menu_type"], meta["year"]
    month1 = date1[0]
    month2 = date2[0]
    day1 = date1[1]
    day2 = date2[1]
    urllist = list()
    remainder = 0
    data = ps.request(rf'https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{str(month1)}/{str(day1)}')
    month = int(data['start_date'].split('-')[1])
    day = int(data['start_date'].split('-')[2])

    month_range = range(month, month2 + 1)
    for months in month_range:
        month = months
        month_len = check_len(month)
        if months == month1:
            while day <= month_len:
                urllist.append(rf'https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}')
                day += 7
            remainder = month_len - day
        else:
            if months != month2:
                day = remainder
                while day <= month_len:
                    urllist.append(rf'https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}')
                    day += 7
                remainder = month_len - day
            else:
                while day <= day2:
                    urllist.append(rf'https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}')
                    day += 7
    return urllist
"""