from music_qa.question import Question
import logging

from music_qa.wikidata_mapper import WikidataMapper, QueryType
from music_qa.sparql_query import run_query
from music_qa.thesaurus import entity_special_case, property_special_case


class XofYQuestion(Question):
    def __init__(self, question, entity, property):
        super(XofYQuestion, self).__init__(question)
        self.mapper = WikidataMapper()
        self.entity = entity
        self.property = property
        self.query = """
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

        query = self.query.format(property_uri=property_uri, entity_uri=entity_uri)
        return run_query(query)

    def extract_entity(self):
        pass


class XofYWhoQuestion(XofYQuestion):
    def __init__(self, question, entity, property):
        super(XofYWhoQuestion, self).__init__(question, entity, property)


class XofYWhatQuestion(XofYQuestion):
    def __init__(self, question, entity, property):
        super(XofYWhatQuestion, self).__init__(question, entity, property)


class XofYWhenQuestion(XofYQuestion):
    def __init__(self, question, entity, property):
        super(XofYWhenQuestion, self).__init__(question, entity, property)


class XofYWhereQuestion(XofYQuestion):
    def __init__(self, question, entity, property):
        super(XofYWhereQuestion, self).__init__(question, entity, property)

    def primary_strategy(self):
        property = property_special_case(self.property)
        entity = entity_special_case(self.entity)
        property_map = self.mapper.get_closest_map(
            "place of {}".format(property), QueryType.PROPERTY
        )
        if not property_map:
            property_map = self.mapper.get_closest_map(property, QueryType.PROPERTY)

        entity_map = self.mapper.get_closest_map(entity, QueryType.ENTITY)

        if not property_map or not entity_map:
            return None

        property_uri = property_map["uri"]
        entity_uri = entity_map["uri"]

        query = self.query.format(property_uri=property_uri, entity_uri=entity_uri)
        return run_query(query)

    def fallback_strategy(self):
        entity = entity_special_case(self.entity)
        property = "country of origin"
        property_map = self.mapper.get_closest_map(property, QueryType.PROPERTY)

        entity_map = self.mapper.get_closest_map(entity, QueryType.ENTITY)

        if not property_map or not entity_map:
            return None

        property_uri = property_map["uri"]
        entity_uri = entity_map["uri"]

        query = self.query.format(property_uri=property_uri, entity_uri=entity_uri)
        return run_query(query)


class XofYHowQuestion(XofYQuestion):
    def __init__(self, question, entity, property):
        super(XofYHowQuestion, self).__init__(question, entity, property)

    def primary_strategy(self):
        property = property_special_case(self.property)
        entity = entity_special_case(self.entity)
        property_map = self.mapper.get_closest_map(
            "cause of {}".format(property), QueryType.PROPERTY
        )
        if not property_map:
            property_map = self.mapper.get_closest_map(property, QueryType.PROPERTY)

        entity_map = self.mapper.get_closest_map(entity, QueryType.ENTITY)

        if not property_map or not entity_map:
            return None

        property_uri = property_map["uri"]
        entity_uri = entity_map["uri"]

        query = self.query.format(property_uri=property_uri, entity_uri=entity_uri)
        return run_query(query)
