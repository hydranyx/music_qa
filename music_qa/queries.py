import itertools
import requests
import sys
import urllib.parse
import random
from question_clf import *
from .mappings import *

NLP = spacy.load("en_core_web_sm")
NLP.vocab["name"].is_stop = False

SPARQL_URL = "https://query.wikidata.org/sparql"


def run_query(query):
    """ Run the provided query string on the Wikidata SPARQL Endpoint. """
    # Prepare the url
    full_url = SPARQL_URL + "?query=" + urllib.parse.quote_plus(query)
    # Prepare the parameters asking for JSON
    params = {"language": "en", "format": "json"}
    # Make the request
    result = requests.get(full_url, params)

    # If the request was unsuccesful
    if result.status_code != 200:
        print("Error communicating with SPARQL end point")
        print(result.url)
        sys.exit()

    # If there are results
    result = result.json()
    if result["results"]["bindings"]:
        return result

    return None


def x_of_y(question):
    """ Create and fire the query to the wikidata endpoint based on a property `property`
    and an entity `entity` """
    property, entity = extract_features(question)
    property = map_property_uri(property)
    entity = map_entity_uri(entity)

    if property and entity:
        query = """
        SELECT DISTINCT ?entityLabel WHERE {{
        wd:{} wdt:{} ?entity.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """.format(
            entity, property
        )
        return run_query(query)

    return None


def description(question):
    # get the
    property = extract_property(question)
    property = map_property_uri(property)

    if property:
        return property["description"]
    return None


def find_boolean_answer(question):
    print(
        """Example questions:
        Did Mozart play on violin?
        Is Sting a woman?
        Is deadmau5 only a composer?
        Is Miley Cyrus the daughter of country singer Billy Ray Cyrus?
        Is Robin Schulz man or woman?
        Is Shakira a model?
        Is the founder of the band DIO still alive?
        Is Dancing Queen an album?
        Do the Beatles have four members? (badly formulated)
        """
    )
    # extract property and item of the question
    # might not work this way and need extract_features()
    property = extract_property(question)
    item = extract_item(question)  # haven't made item yet
    property = map_property_uri(property)

    if property and item:
        # gets a match on a specific item for a give property
        type1 = list_type1(property, item)
        if type1:
            # if it is a count question asking if it is the only item ask:
            if only_item_question(question):
                return list_only(property, item)
            return True
        # needs more types and some expansion but this is selective search
        # if not type1 then check list_type2, list_type3 etc. which is broader
        return False


def boolean(question):

    answer = find_boolean_answer(question)
    if answer:
        return answer
    # if no answer found, generate one
    rand = random.randint(0, 1)
    answer = "yes" if (rand == 0) else "no"
    # return random answer
    return answer


def list_only(property, item):
    print(
        "List question that needs to check if it's feature is findable and if it is the **only** property of the regarding relation."
    )
    query = """
    SELECT (COUNT (?item2) as ?count) WHERE {{
    {} ?p ?item.
    ?item rdfs:label ?itemLabel.
    {} ?p ?item2
 
    FILTER (LANG (?itemLabel) = 'en')  
    FILTER REGEX (?itemLabel,{}).
    }}""".format(
        property, property, item
    )
    count = run_query(query)
    if count < 1:
        # NOTE: something is wrong and known_associates should be used
        return False
    if count == 1:
        return True
    if count > 1:
        return False


def know_associates(word):
    query = """
        SELECT DISTINCT ?itemLabel WHERE {{
        {} skos:altLabel ?itemLabel
        FILTER (LANG (?itemLabel) = 'en')
        }}
        """.format(
        word
    )
    # returns an 'Also known as' words list
    return run_query(query)


def list_type1(property, item):
    query = """
    SELECT DISTINCT ?p ?itemLabel WHERE {{
    {} ?p ?item.
    ?item rdfs:label ?itemLabel
    
    FILTER (LANG (?itemLabel) = 'en')
    FILTER REGEX (?itemLabel, {}).
    }}
    """.format(
        property, item
    )
    # returns
    return run_query(query)
