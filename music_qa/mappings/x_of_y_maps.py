import itertools
import requests
import spacy
import sys
import urllib.parse

NLP = spacy.load("en_core_web_sm")
NLP.vocab["name"].is_stop = False

API_URL = "https://www.wikidata.org/w/api.php"
SPARQL_URL = "https://query.wikidata.org/sparql"


def get_close_properties(property):
    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "type": "property",
        "search": property,
    }
    json = requests.get(API_URL, params).json()
    try:
        properties = [
            (result["id"], result["label"], result["description"])
            for result in json["search"]
        ]
    except IndexError:
        properties = []
    except KeyError:
        print("The API seems to be providing malformed JSON. Perhaps a rate limit?")
        print("The JSON is:")
        print(json)
        sys.exit()
    return properties


def map_property_uri(property):
    """ Map a provided string to the property URI """
    try:
        property = get_close_properties(property)[0][0]
    except IndexError:
        property = None
    return property


def get_close_entities(entity):
    params = {
        "action": "wbsearchentities",
        "language": "en",
        "format": "json",
        "search": entity,
    }
    json = requests.get(API_URL, params).json()
    try:
        entities = [(result["id"], result["label"]) for result in json["search"]]
    except IndexError:
        entities = []
    except KeyError as exception:
        print("The API seems to be providing malformed JSON. Perhaps a rate limit?")
        print(json)
        raise exception
    return entities


def map_entity_uri(entity):
    """ Map a provided string to the entity URI """
    try:
        entity = get_close_entities(entity)[0][0]
    except IndexError:
        entity = None
    return entity
