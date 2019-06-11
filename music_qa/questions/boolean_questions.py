from music_qa.question import Question
import logging
import random

from music_qa.sparql_query import run_query
from music_qa.wikidata_mapper import WikidataMapper, QueryType


class BooleanQuestion(Question):
    def __init__(self, question, attribute, entity):
        super(BooleanQuestion, self).__init__(question)
        self.mapper = WikidataMapper()
        self.attribute = attribute
        self.entity = entity
        self.query = """
        SELECT DISTINCT ?itemLabel WHERE {{
        wd:{entity_uri} ?p ?item.
        ?item rdfs:label ?itemLabel

        FILTER (LANG (?itemLabel) = 'en')
        FILTER REGEX (?itemLabel, "{attribute}").
        }}
        """

    def primary_strategy(self):
        entity_map = self.mapper.get_closest_map(self.entity, QueryType.ENTITY)
        if not entity_map:
            return None

        entity_uri = entity_map["uri"]
        query = self.query.format(entity_uri=entity_uri, attribute=self.attribute)
        result = run_query(query)
        logging.debug(query)
        logging.info("Boolean question result: %s", result)
        if result is not None:
            logging.debug("Boolean question result: %s", result)
            # Since there is a result there is a property with the attribute as a result via wikidata
            return True
        else:
            return False

    def fallback_strategy(self):
        return False


class BooleanOnlyQuestion(BooleanQuestion):
    def __init__(self, question, attribute, entity):
        super(BooleanOnlyQuestion, self).__init__(question, attribute, entity)
        self.mapper = WikidataMapper()
        self.query = """
        SELECT ?item2Label WHERE {{
        wd:{entity_uri} ?p ?item.
        ?item rdfs:label ?itemFilterTerm.
        wd:{entity_uri} ?p ?item2.


        FILTER (LANG (?itemFilterTerm) = 'en')
        FILTER REGEX (?itemFilterTerm,"{attribute}").
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".}}
        }}
        """

    def primary_strategy(self):
        entity_map = self.mapper.get_closest_map(self.entity, QueryType.ENTITY)
        if not entity_map:
            return None

        entity_uri = entity_map["uri"]
        query = self.query.format(entity_uri=entity_uri, attribute=self.attribute)
        result = run_query(query)
        if result is not None:
            logging.debug("Boolean question result: %s", result)
            if len(result) == 1:
                return True
            elif len(result) > 1:
                return False

        return None

    def fallback_strategy(self):
        # If there is no matching answer, i.e. no result or len(result) == 0, then we don't have enough information so the fallback should be run.
        return random.choice([True, False])
