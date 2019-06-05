from nltk.corpus import wordnet
import sys
import requests
import re

def get_wikidata(text, use):

    url = 'https://www.wikidata.org/w/api.php'
    params = {'action':'wbsearchentities', 'language':'en', 'format':'json'}

    info = []

    if use == 'entity':
        pass
    elif use == 'property':
        params['type'] = 'property'
    else:
        print('uncorrect call, specify type of info(entity/property) as second argument')
        return info
    
    words = []
    
    words.append(text)

    synonyms = []

    for word in words:

        params['search'] = word
        json = requests.get(url, params).json()
                
        for result in json['search']:
            info.append(result['id'])

        if info:
            break

        if not synonyms:    
            synonyms = wordnet.synsets(text)    

            for synonym in synonyms:
                a = synonym.lemmas()[0].name()
                b = a.replace("_"," ")
                words.append(b)

    return info