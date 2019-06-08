from enum import Enum
import re
import logging
import spacy
from .question import (
    BooleanQuestion,
    CountQuestion,
    DescriptiveQuestion,
    HighestQuestion,
    ListQuestion,
    QualifiedQuestion,
)

from .wikidata_mapper import QueryType


class QuestionType(Enum):
    BOOLEAN = 1
    COUNT = 2
    DESCRIPTION = 3
    HIGHEST = 4
    LIST = 5
    QUALIFIED = 6


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.question_switch = {
            QuestionType.BOOLEAN: BooleanQuestion,
            QuestionType.COUNT: CountQuestion,
            QuestionType.DESCRIPTION: DescriptiveQuestion,
            QuestionType.HIGHEST: HighestQuestion,
            QuestionType.LIST: ListQuestion,
            QuestionType.QUALIFIED: QualifiedQuestion,
        }

    def prepare_question(self, question):
        # classify the question somehow
        question_type = self.determine_question_type(question)
        logging.debug("Question: %s determined to be %s", question, question_type)
        features = self.extract_features(question, question_type)
        logging.debug("Question: %s has features %s", question, features)
        question = self.question_switch[question_type](question, *features)
        return question

    def determine_question_type(self, question):
        doc = self.nlp(question)

        # HIGHEST Question
        m = re.search(
            "(?:highest|lowest|first|last|oldest|youngest|earliest|latest)",
            question,
            re.IGNORECASE,
        )
        if m is not None:
            return QuestionType.HIGHEST

        # BOOLEAN Question
        if doc[0].tag_[0] == "V":
            return QuestionType.BOOLEAN

        # COUNT Question
        m = re.search("(?:How) (?:many|much)", question, re.IGNORECASE)
        if m is not None:
            return QuestionType.COUNT

        # DESCRIPTION Question
        # TODO IN LIST
        m = re.search("(?:What|Who) (Is|Was)", question, re.IGNORECASE)
        if m is not None:
            return QuestionType.DESCRIPTION

        # LIST Question
        m = re.search("(?:What|Who|Where|When)", question, re.IGNORECASE)
        m2 = re.search("(?:In) (?:What|Which)", question, re.IGNORECASE)
        m3 = re.search("(?:Which)", question, re.IGNORECASE)
        m4 = re.search("(?:How did)", question, re.IGNORECASE)
        if m is not None or m2 is not None or m3 is not None or m4 is not None:
            return QuestionType.LIST

        return QuestionType.LIST

    def extract_features(self, question, question_type):
        if question_type == QuestionType.DESCRIPTION:
            return [QueryType.ENTITY]
        return ("property", "entity")
