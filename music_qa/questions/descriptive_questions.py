from music_qa.question import Question
import logging


from music_qa.wikidata_mapper import WikidataMapper, QueryType


class DescribeEntityQuestion(Question):
    def __init__(self, question, entity):
        super(DescribeEntityQuestion, self).__init__(question)
        self.entity = entity
        self.mapper = WikidataMapper()

    def primary_strategy(self):
        mapping = self.mapper.get_closest_map(self.entity, QueryType.ENTITY)
        if mapping is None:
            return None

        label = mapping["label"]
        description = mapping["description"]
        if description:
            return "{}".format(label)
        else:
            return "{}: {}".format(label, description)

    def extract_entity(self):
        pass


class DescribePropertyQuestion(Question):
    def __init__(self, question, property):
        super(DescribePropertyQuestion, self).__init__(question)
        self.mapper = WikidataMapper()
        self.property = property

    def primary_strategy(self):
        mapping = self.mapper.get_closest_map(self.property, QueryType.PROPERTY)
        if mapping is None:
            return None

        label = mapping["label"]
        description = mapping["description"]
        if description:
            return "{}".format(label)
        else:
            return "{}: {}".format(label, description)

    def extract_property(self):
        pass
