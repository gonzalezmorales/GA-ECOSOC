import re
import json
import utils
import json

#json_file =  'output/GA_74.json'
json_file =  'output/ECOSOC_2020.json'


#txt_file =  'output/GA_74.txt'
txt_file =  'output/ECOSOC_2020.txt'

resolutions_json_data = json.load(open(json_file))

keywords = ["data", "statistic", "indicator", "geospatial"]

for r in resolutions_json_data:
    print(f'resolution = {r["resolution"]}')
    print(f'date = {r["date"]}')
    print(f'title = {r["title"]}')
    print(f'session = {r["session"]}')
    print(f'agendaItem = {r["agendaItem"]}')

#Add resolution information to a tab-delimited text file:

data = []

for r in resolutions_json_data:

    for c in r["content"]:

        p = dict()

        p["resolution"] = r["resolution"]
        p['date']=r["date"]
        p['title']=r["title"]
        p['session']=r["session"]
        p['agendaItem']=r["agendaItem"]

        p["content"] = re.sub('\s+',' ',c)

        k_list = []

        for k in keywords:
            if k.lower() in c.lower():
                k_list.append(k)

        p['keywords'] = k_list 

        data.append(p)

    

utils.dictList2tsv(data, txt_file)

  