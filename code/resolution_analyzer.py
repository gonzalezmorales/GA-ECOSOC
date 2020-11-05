# import required libraries
import tika
from tika import parser
tika.initVM()
import re
import json
import csv
import requests
import utils

# choose: GA or ECOSOC?

UNBody = 'ECOSOC' 
# UNBody = 'GA'

if UNBody == 'ECOSOC':
  UNBodyName = 'The Economic and Social Council'
  documentCodePrfx = 'E/2020/'
  session = '2020 session'
  output_json = 'ECOSOC_2020.json'
  output_txt = 'ECOSOC_2020.txt'  
elif UNBody == 'GA':
  UNBodyName = 'The General Assembly'
  documentCodePrfx = 'A/RES/74/'
  session = 'Seventy-fourth session'
  output_json = 'GA_74.json'
  output_txt = 'GA_74.txt'  


links_catalog = 'ResolutionLinks/'+ UNBody +'.txt'


# read resolution catalogue into dictionary

resolutions = utils.tsv2dictlist(links_catalog)

failed = []
output = []

# for each resolution:
for r in resolutions:
  # Read the word document

  try:

    url = r['URL2']
    response = requests.get(url)
    parsed = parser.from_buffer(response)
    raw = parsed['content']

    #Remove extra line breaks, unnecessary white space, and other characters
    raw = re.sub('\n\s+','\n',raw).replace(u'\xa0', u' ').replace(u'\u2212',u'-').replace(u'\u200e','')

    print('----------------------------------------------------------------------')

    #Create an array with each paragraph as an element
    contentElements = raw.split(UNBodyName,1)[1].splitlines()
    print(documentCodePrfx)
    print(re.search(re.escape(documentCodePrfx) + r'(.*?)\n', raw))

    metadata =	{
        "resolution": r['Resolution'],
        "date": re.search('Distr.: (.*?)\n(.*?)\n', raw).group(2),
        "title": r['Title'],
        "session": session,
        "agendaItem" : re.search(re.escape(session) + r'(.*?)\n(.+?)\n', raw).group(2),
        "content" : contentElements
      }

    print(f'metadata={metadata}')


    output.append(metadata)
    
    print('----------------------------------------------------------------------')
  except:
    print(url)
    failed.append(url)
    print('----------------------------------------------------------------------')




output_path = 'output/'

#with open('resolutions.json', 'w') as outfile:
with open(output_path + output_json, 'w') as outfile:
    json.dump(output,outfile, indent=4 )    

resolutions_json_data = json.load(open(output_path +  output_json))

for r in resolutions_json_data:
    print(r["resolution"])
    print(r["date"])
    print(r["title"])
    print(r["session"])
    print(r["agendaItem"])
    print(r["content"][0])

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