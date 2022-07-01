import json
import requests

def save(data):
    with open(file=input("filename to write json object to: ") + '.json', mode='w') as file:
        json.dump(data, file)

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

def collect_day(day):
    school_info = {
        "prefix": 'hawaiiprep',
        "school_id": '6812',
        "menu_type": '3106',
    }
    url = day_url(day)
    data = request(url)
    menudict = dataparser(data)
    return menudict

def request(url):
    data = requests.get(url).json()
    return data

def day_url(date, meta):
    prefix, school_id, menu_type = meta["prefix"], meta["school_id"], meta["menu_type"]
    month, day, year = date[0], date[1], date[2]
    url = rf"https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}"
    return url

def dataparser(data, include_ingredients=True, include_nutrition_data=True):
    menudict = dict()
    print(data)
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
            station_list = ["Entree/Sides", "Vegetarian", "Pizza, Flatbreads", "Chefs Table", "Deli", "Vegan"]
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


