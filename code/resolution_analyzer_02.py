
resolutions_json_data = json.load(open(output_path +  output_json))

for r in resolutions_json_data:
    print(f'resolution = {r["resolution"]}')
    print(f'date = {r["date"]}')
    print(f'title = {r["title"]}')
    print(f'session = {r["session"]}')
    print(f'agendaItem = {r["agendaItem"]}')

#Add resolution information to a tab-delimited text file:
outF = open(output_path + '\\' + output_txt, "w")
for r in resolutions_json_data:
    for c in r["content"]:
        has_keywords = ""
        for k in keywords:
            if k.lower() in c.lower():
                has_keywords = has_keywords + k + ", "
        line = r["resolution"]+"\t" \
               + r["date"]+"\t" \
               + r["title"].replace('\t','   ')+"\t" \
               + r["session"]+"\t" \
               + r["agendaItem"]+"\t" \
               + c.replace('\t','   ')+"\t" \
               + has_keywords
        outF.write(line)
        outF.write("\n")
outF.close()    