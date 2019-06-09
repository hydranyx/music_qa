import logging
import re
import spacy
from .question import (
    QuestionType,
    BooleanQuestion,
    CountQuestion,
    DescriptiveQuestion,
    HighestQuestion,
    ListQuestion,
    QualifiedQuestion,
)

from .wikidata_mapper import QueryType
from .classifier import Classifier


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.classifier = Classifier()
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
        question_type = self.classifier.classify(question)
        logging.debug("Question: %s determined to be %s", question, question_type)
        features = self.extract_features(question, question_type)
        logging.debug("Question: %s has features %s", question, features)
        question = self.question_switch[question_type](question, *features)
        return question

    def extract_features(self, question, question_type):
        """
        A function to extract features needed for querying. The returned list
        should be the same length as the number of arguments in the __init__ of
        the question matching the question type (aside from the initial
        question parameter).
        """
        if question_type == QuestionType.DESCRIPTION:
            # TODO determine which type of descriptive question.
            # If entity only return QueryType.ENTITY
            # If property only return QueryType.PROPERTY
            return [QueryType.ENTITY]
        if question_type == QuestionType.LIST:
            return [QueryType.PROPERTY, QueryType.ENTITY]
        logging.debug("Extracting features for question type %s", question_type)
        return ("property", "entity")
