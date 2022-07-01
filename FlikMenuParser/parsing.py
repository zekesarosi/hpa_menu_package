import requests
import json



def request(url):
    data = requests.get(url).json()
    return data

def day_url(date, meta):
    prefix, school_id, menu_type = meta["prefix"], meta["school_id"], meta["menu_type"]
    month, day, year = date[0], date[1], date[2]
    url = rf"https://{prefix}.flikisdining.com/menu/api/weeks/school/{school_id}/menu-type/{menu_type}/{year}/{month}/{day}"
    return url

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
                    daylist.append({
                        "name": food_dict['name'],
                        "ingredients": food_dict["ingredients"].split(","),
                        "nutrition info": food_dict["rounded_nutrition_info"],
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
}
if __name__ == "__main__":
    date = ["04", "22", "2022"]
    print(collect_day(date, school_info))
