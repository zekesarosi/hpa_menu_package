import requests
import json
from FlikMenuParser.get_url import day_url


def request(url):
    data = requests.get(url).json()
    return data

def dataparser(data):
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
                    daylist.append(food_dict['name'])
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



def save(data):
    with open(file=input("filename to write json object to: ") + '.json', mode='w') as file:
        json.dump(data, file)

def collect_day(day, meta):
    url = day_url(day, meta)
    data = request(url)
    menudict = dataparser(data)
    save(menudict)

school_info = {
    "prefix": 'hawaiiprep',
    "school_id": '6812',
    "menu_type": '3106',
    "year": '2022',
}
date = ["04", "22"]

print(collect_day(date, school_info))
