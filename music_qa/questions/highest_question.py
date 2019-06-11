from music_qa.question import Question
import logging
import random

from music_qa.sparql_query import run_query
from music_qa.wikidata_mapper import WikidataMapper, QueryType


class HighestQuestion(Question):
    def __init__(self, question, attribute, entity):
        super(HighestQuestion, self).__init__(question)
        self.mapper = WikidataMapper()

    def primary_strategy(self):
        return None
