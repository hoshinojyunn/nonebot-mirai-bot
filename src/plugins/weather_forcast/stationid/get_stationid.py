import json

with open('city_data.json', 'r') as f:
    city_list = eval(f.read())

city_dict = {}

for i in city_list:
    city_dict[i["city"]] = i["code"]

with open("city_code.json",'w') as fp:
    json.dump(city_dict, fp, ensure_ascii=False, indent=4, sort_keys=True)
