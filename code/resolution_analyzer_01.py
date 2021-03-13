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
session = '2020' 
session_desc = '2020 session'


# UNBody = 'GA'
# session = '75' 
# session_desc = 'Seventy-fourth session'

if UNBody == 'ECOSOC':
  UNBodyName = 'The Economic and Social Council'
  documentCodePrfx = 'E/'+ session
  output_json = 'ECOSOC_' + session + '.json'
  output_txt = 'ECOSOC_' + session + '.txt'  
elif UNBody == 'GA':
  UNBodyName = 'The General Assembly'
  documentCodePrfx = 'A/RES/' + session + '/'
  output_json = 'GA_' + session + '.json'
  output_txt = 'GA_' + session + '.txt'  

# read resolution catalogue into dictionary

resolutions = utils.tsv2dictlist('ResolutionLinks/' + output_txt)

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
    raw = re.sub('\n\s+','\n',raw).replace(u'\xa0', u' ').replace(u'\u2212',u'-').replace(u'\u200e','').replace(u'\u2013','-')

    #Create an array with each paragraph as an element
    test = raw.split(UNBodyName,1)[1]

    # for t in test:
    #   t = re.sub('\v+','',t)

    contentElements = test.splitlines()

    contentElements =  [x for x in contentElements if x not in [',', ', ']]

    print(documentCodePrfx)

    #print(re.search(re.escape(documentCodePrfx) + r'(.*?)\n', raw))

    metadata =	{
        "resolution": r['Resolution'],
        "date": re.search('Distr.: (.*?)\n(.*?)\n', raw).group(2),
        "title": r['Title'],
        "session": session,
        "agendaItem" : re.search(re.escape(session) + r'(.*?)\n(.+?)\n', raw).group(2),
        "content" : contentElements
      }

    #print(f'metadata={metadata}')


    output.append(metadata)
    

  except:
    print('----------------------------------------------------------------------')
    print(url)
    failed.append(url)
    print('----------------------------------------------------------------------')


output_path = 'output/'

#with open('resolutions.json', 'w') as outfile:
with open(output_path + output_json, 'w') as outfile:
    json.dump(output,outfile, indent=4 )    

