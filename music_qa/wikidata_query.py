"""
Run a query to Wikidata
"""

# TODO seperate class for SparQL queries?
from enum import Enum
import itertools
import requests
import sys
import urllib.parse
import random

class QueryType(Enum):
    PROPERTY = "property"
    ENTITY = "entity"


class WikidataQuery:
	def __init__(self):
		self.SPARQL_URL = "https://query.wikidata.org/sparql"

	def run_query(self, query):
	    """ Run the provided query string on the Wikidata SPARQL Endpoint. """
	    # Prepare the url
	    full_url = self.SPARQL_URL + "?query=" + urllib.parse.quote_plus(query)
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


	def know_associates(self, word):
	    query = """
	        SELECT DISTINCT ?itemLabel WHERE {{
	        {} skos:altLabel ?itemLabel
	        FILTER (LANG (?itemLabel) = 'en')
	        }}
	        """.format(
	        word
	    )
	    # returns an 'Also known as' words list
	    return self.run_query(query)


	def x_of_y_q(self, entity, property):
	    # example: What is the birth name of Eminem?
	    query = """
	    SELECT DISTINCT ?entityLabel WHERE {{
	    wd:{} wdt:{} ?entity.
	    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
	    }}
	    """.format(
	        entity, property
	    )
	    # returns a list containing 0 or more phrases.
	    return self.run_query(query)


	def list_only_q(self, property, item):
	    # vb: Is deadmou5 only a composer?
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
	    # returns a number
	    return self.run_query(query)


	def list_type1_q(self, entity, item):
	    # vb: Did Mozart play violin?
	    query = """
	    SELECT DISTINCT ?itemLabel WHERE {{
	    wd:{} ?p ?item.
	    ?item rdfs:label ?itemLabel

	    FILTER (LANG (?itemLabel) = 'en')
	    FILTER REGEX (?itemLabel, "{}").
	    }}
	    """.format(
	        entity, item
	    )
	    # returns the words or word-parts that it found as a match with the phrase item
	    return self.run_query(query)


	def list_type2_q(self, sub_entity, sub_property, main_property):
	    # example: What awards did the band that played Bohemian Rhapsody receive?
	    # for a question with a subquestion
	    # has multiple properties but is not a qualified statement
	    query = """
	    SELECT DISTINCT ?itemLabel WHERE {{
	    wd:{} wdt:{} ?subitem.
	    ?subitem wdt:{} ?item.
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}}
	    """.format(
	        sub_entity, sub_property, main_property
	    )
	    # returns a list of entities
	    return self.run_query(query)


	def qualified_statement_for_time_q(self, entity, property, qualifier):
	    # What were the members of teh Beatles in 1960
	    # P580: start time , for year qualifier
	    # P582: end time, for year qualifier .
	    query = """
	    SELECT ?persLabel WHERE {{
	    BIND (qualifier AS ?year)
	    wd:{} p:{} ?item.
	    ?item pq:P580 ?starttime.
	    ?item pq:P582 ?endtime.
	    ?item ps:{} ?pers.

	    # filter the ?pers by startime ?time being "1960"
	    FILTER (?year >= year(?starttime) && ?year < year(?endtime)).
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}}
	    """.format(
	        qualifier, entity, property, property
	    )
	    return self.run_query(query)


	def qualified_statement_for_qualifier(self, qualifier, quality, entity, property):
	    # vb: What Beatle members are instrumentaists?
	    query = """
	    SELECT ?persLabel WHERE {{

	    # go through all thesaurus qualifiers to find a matching pq
	    BIND (pq:{} AS ?qualifier)

	    BIND (wd:{} AS ?quality)
	    wd:{} p:{} ?item.
	    ?item ps:{} ?pers.
	    ?item ?qualifier ?role.

	    # filter by qualifier
	     FILTER (?quality = ?role).
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}}
	    """.format(
	        qualifier, quality, entity, property, property
	    )
	    # return a list of items
	    return self.run_query(query)
