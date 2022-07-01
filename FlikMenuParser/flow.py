def collect_day(day):
    school_info = {
        "prefix": 'hawaiiprep',
        "school_id": '6812',
        "menu_type": '3106',
    }
    url = day_url(day)
    data = request(url)
    menudict = dataparser(data)
    save(menudict)

def request(url):
    data = requests.get(url).json()
    return data

def day_url(date, meta):
    prefix, school_id, menu_type = meta["prefix"], meta["school_id"], meta["menu_type"]
    month, day, year = date[0], date[1], date[2]
    url = rf"https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}"
    return url