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


