import json
import requests
import threading



def save(data, file_name):
    with open(file=file_name, mode='w') as file:
        json.dump(data, file, indent=4)

def check_len(month, year):
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

def collect_week_multi(date, lock, menulist, nutrition_info=True, ingredients=True):
    url = week_url(date)
    data = request(url)
    menudict = dataparser(data, ingredients, nutrition_info)
    lock.acquire()
    menulist.append(menudict)
    lock.release()
    print(menudict)

def collect_month_multi(date, full_week=False, nutrition_info=True, ingredients=True):
    lock = threading.Lock()
    month_specified = date.split("-")[1]
    date += "-01"
    year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
    start_menu = collect_week(f"{year}-{month}-{day}", nutrition_info=nutrition_info, ingredients=ingredients)
    menu_dict = {}
    weeks = [ele*7 for ele in range(1,3)]
    thread_list = []
    menu_list = [start_menu]
    for day in weeks:
        thread = threading.Thread(target=collect_week_multi, args=[f"{year}-{month}-{day}", lock, menu_list, False, False])
        thread.start()
        thread_list.append(thread)
    for t in thread_list:
        t.join()
    for d in menu_list:
        menu_dict = menu_dict | d
    delete = []
    if not full_week:
        for date in menu_dict.keys():
            year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
            if month != month_specified:
                delete.append(date)
        for i in delete:
            del menu_dict[i]
    return menu_dict

# Pass in a month and a year. YY-MM. Either include or exclude Nutrition Info / Ingredients. full_week param when
# True will include a whole weeks data even if some days in the begginning or ending week doesn't occur in the given
# month. For example if Feb 1 is a thursday, the dataset will also include the Mon Tues Wed of the previous January.
def collect_month(date, meal='lunch', full_week=False, nutrition_info=True, ingredients=True):
    month_specified = date.split("-")[1]
    date += "-01"
    year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
    start_menu = collect_week(f"{year}-{month}-{day}", meal, nutrition_info=nutrition_info, ingredients=ingredients)
    menu_dict = {}
    menu_list = [start_menu]
    cycling = True
    while cycling:
        day = ("0" + str(int(day) + 7) if int(day) < 3 else int(day) + 7)
        week_menu = collect_week(f"{year}-{month}-{day}", meal, nutrition_info=nutrition_info, ingredients=ingredients)
        menu_list.append(week_menu)
        if int(day) >= check_len(month, year):
            cycling = False
    for d in menu_list:
        menu_dict = menu_dict | d
    delete = []
    if not full_week:
        for date in menu_dict.keys():
            year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
            if month != month_specified:
                delete.append(date)
        for i in delete:
            del menu_dict[i]
    return menu_dict


def collect_week(date, meal='lunch', nutrition_info=True, ingredients=True):
    url = week_url(date, meal)
    data = request(url)
    menudict = dataparser(data, meal, ingredients, nutrition_info)

    return menudict

def request(url):
    try:
        data = requests.get(url)
        return json.loads(data.text)
    except Exception as e:
        print(e)
        exit()


def week_url(date, meal):
    school_info = {
        "prefix": 'hawaiiprep.api',
        "school_id": 'hawaii-preparatory-academy',
        "menu_type": meal,
    }
    meta = school_info
    date = date.split("-")
    prefix, school_id, menu_type = meta["prefix"], meta["school_id"], meta["menu_type"]
    year, month, day = date[0], date[1], date[2]
    url = rf"https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}"
    return url

def dataparser(data, meal, include_ingredients=True, include_nutrition_data=True):
    menudict = dict()
    for day in data['days']:
        if len(day['menu_items']) != 0:
            date = day['date']
            menudict[date] = []
            daylist = list()
            for info in day['menu_items']:
                if len(info['text']) > 1:
                    station_name = info['text']
                    daylist.append(station_name)
                else:
                    food_dict = info["food"]
                    if include_ingredients and include_nutrition_data:
                        daylist.append({
                        "name": food_dict['name'],
                        "ingredients": food_dict["ingredients"].split(","),
                        "nutrition info": food_dict["rounded_nutrition_info"],
                        })
                    elif include_nutrition_data and not include_ingredients:
                        daylist.append({
                            "name": food_dict['name'],
                            "nutrition info": food_dict["rounded_nutrition_info"],
                        })
                    elif include_ingredients and not include_nutrition_data:
                        daylist.append({
                            "name": food_dict['name'],
                            "ingredients": food_dict["ingredients"].split(","),
                        })
                    elif not include_ingredients and not include_nutrition_data:
                        daylist.append({
                            "name": food_dict['name']
                        })
            if meal.lower() == 'dinner':
                station_list = ["Entree/Sides","Chefs Table Dinner"]
            elif meal.lower() == 'lunch':
                station_list = ["Entree/Sides", "Chefs Table", "Soup"]
            elif meal.lower() == 'breakfast':
                station_list = ["Breakfast Specials"]
            elif meal.lower() == 'brunch':
                station_list = ["Entree/Sides"]
            station_index_a = 0
            day_dict = {}
            ind = 1
            for stations in station_list:
                try:
                    station_index = daylist.index(station_list[ind])
                except:
                    station_index = len(daylist)
                dishes = [dish for dish in daylist[(station_index_a + 1) : (station_index)]]
                station_index_a = station_index
                ind += 1
                day_dict[stations] = dishes
            menudict[date] = day_dict
    return menudict


