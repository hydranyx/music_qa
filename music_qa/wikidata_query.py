"""
Run a query to Wikidata
"""

# TODO seperate class for SparQL queries?
from enum import Enum


class QueryType(Enum):
    PROPERTY = "property"
    ENTITY = "entity"


class WikidataQuery:
    pass
