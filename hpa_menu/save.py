import json

def save(data):
    with open(file=input("filename to write json object to: ") + '.json', mode='w') as file:
        json.dump(data, file)
