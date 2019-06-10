from music_qa.question import Question
import logging

from music_qa.wikidata_mapper import WikidataMapper, QueryType


class CountQuestion(Question):
    def __init__(self, question):
        super(CountQuestion, self).__init__(question)
        self.mapper = WikidataMapper()

    def primary_strategy(self):
        return None
