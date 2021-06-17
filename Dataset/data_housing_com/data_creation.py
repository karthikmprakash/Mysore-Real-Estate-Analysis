# Data is extracted from www.housing.com
# initially the data is manually copy pasted from the ajax responses as the page was dynamically loaded as scrolled 
# the json data in the text file jsons.txt is loaded and cleaned to extract thekey value pairs which are vital for the project 

import json

with open('jsons.txt','r',encoding="utf8") as f:
    line = f.readlines()
    
location_list = []
beds_list = []
price_list = []
area_list = []


for n in range(len(line)-1):
    if line[n] != '\n':  
        data = json.loads(line[n])['data']
        search_result = data['searchResults']
        properties = search_result['properties']
        
        for i in range(len(properties)-1):
            location_list.append(properties[i]['address']['address'])
            area_list.append(properties[i]['builtUpArea'])
            beds_list.append(properties[i]['title'])
            price_list.append(properties[i]['displayPrice']['value'])
        