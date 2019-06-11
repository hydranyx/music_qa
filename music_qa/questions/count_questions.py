from music_qa.question import Question
import logging

from music_qa.wikidata_mapper import WikidataMapper, QueryType
from music_qa.sparql_query import run_query
from music_qa.thesaurus import entity_special_case, property_special_case

from ..util import (
    extract_entity,
    extract_property,
    get_words_and_dep,
    get_word_by_dep,
    extract_entity_boolean,
    extract_property_boolean,
)


class CountQuestion(Question):
    def __init__(self, question, entity, property):
        super(CountQuestion, self).__init__(question)
        self.mapper = WikidataMapper()
        self.entity = entity
        self.property = property
        self.primary_query = """
        SELECT (COUNT (?item) as ?count) WHERE {{
        wd:{entity_uri} wdt:{property_uri} ?item
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """
        self.fallback_query = """
        SELECT DISTINCT ?entityLabel WHERE {{
        wd:{entity_uri} wdt:{property_uri} ?entity.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """

    def primary_strategy(self):
        property = property_special_case(self.property)
        entity = entity_special_case(self.entity)
        property_map = self.mapper.get_closest_map(property, QueryType.PROPERTY)
        entity_map = self.mapper.get_closest_map(entity, QueryType.ENTITY)

        if not property_map or not entity_map:
            return None

        property_uri = property_map["uri"]
        entity_uri = entity_map["uri"]

        query = self.primary_query.format(
            property_uri=property_uri, entity_uri=entity_uri
        )
        result = run_query(query)
        if result:
            answer = int(result[0])
            if answer > 0:
                return answer
        return None

    def fallback_strategy(self):
        # if this one doesn't find a match return zero
        property = property_special_case(self.property)
        entity = entity_special_case(self.entity)
        property_map = self.mapper.get_closest_map(
            "number of {}".format(property), QueryType.PROPERTY
        )
        entity_map = self.mapper.get_closest_map(entity, QueryType.ENTITY)

        if not property_map or not entity_map:
            return None

        property_uri = property_map["uri"]
        entity_uri = entity_map["uri"]

        query = self.fallback_query.format(
            property_uri=property_uri, entity_uri=entity_uri
        )

        result = run_query(query)
        if result:
            answer = int(result[0])
            if answer > 0:
                return answer
        return 0
