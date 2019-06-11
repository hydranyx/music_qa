"""
A question as interpreted by the QA system.
"""

import logging
import random
import spacy
import itertools
from music_qa.wikidata_mapper import WikidataMapper, QueryType
from abc import ABC, abstractmethod


# TODO don't reload the spacy model
NLP = spacy.load("en_core_web_sm")


class Question(ABC):
    """
    A base question as used by the QA system.
    """

    def __init__(self, question):
        self.question = question

    def __str__(self):
        return "Question: " + self.question

    @abstractmethod
    def primary_strategy(self):
        pass

    def fallback_strategy(self):
        return None

    def execute(self):
        result = self.primary_strategy()
        if result is None:
            result = self.fallback_strategy()
        return result
