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
from .question import QuestionType
from nltk import wordnet


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en")
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
        print(question_type)
        question.add_features(features)
        return question

    def extract_features(self, question, question_type):
        if question_type is QuestionType.LIST:
            result = list_question(question, self.nlp)
        elif question_type is QuestionType.BOOLEAN:
            result = boolean_question(question, self.nlp)
        elif question_type is QuestionType.COUNT:
            result = count_question(question, self.nlp)
        elif question_type is QuestionType.HIGHEST:
            result = highest_question(question, self.nlp)
        elif question_type is QuestionType.QUALIFIED:
            result = qualified_question(question, self.nlp)
        elif question_type is QuestionType.DESCRIPTION:
            result = description_question(question, self.nlp)
        return result


def list_question(question, nlp):
    return ("property example", "entity example")


def boolean_question(question, nlp):
    # Getting the individual words, and the dependencies
    words, dep_list = get_words_and_dep(question, nlp)

    # Try to get an entity
    ent = get_word_by_dep(words, dep_list, "nsubj")

    ##If there is an entity, try to get a attribute
    if ent:
        attr = get_word_by_dep(words, dep_list, "attr")

        # If there is no attr, often the dobj is the attribute
        if not attr:
            attr = get_word_by_dep(words, dep_list, "dobj")

        if not attr:
            attr = get_word_by_dep(words, dep_list, "pobj")

        # If this is also not the case, often the verb/root is the attribute
        if not attr:
            attr = get_word_by_dep(words, dep_list, "ROOT")

    # If there is no entity, often the ROOT is the entity and dobj the attribute (e.g. Is rapping a music style?)
    else:
        ent = get_word_by_dep(words, dep_list, "ROOT")
        attr = get_word_by_dep(words, dep_list, "dobj")
        if not attr:
            attr = get_word_by_dep(words, dep_list, "pobj")

    # TODO a boolean question has another pair of words (not a prop, but a attr)
    return {"attribute": attr, "entity": ent}


def count_question(question, nlp):
    # print(question)
    return {"property": prop, "entity": entities}


def highest_question(question, nlp):

    words, dep_list = get_words_and_dep(question, nlp)

    prop = (
        get_word_by_dep(words, dep_list, "amod")
        + " "
        + get_word_by_dep(words, dep_list, "nsubj")
    )

    ent = get_word_by_dep(words, dep_list, "pobj")

    ent.strip()
    prop.strip()

    return {"property": prop, "entity": ent}


def qualified_question(question, nlp):
    print(question)


def description_question(question, nlp):

    parse = nlp(question)

    prop = ""
    ent = ""

    for w in parse:
        if w.tag_ in ["NN", "NNS", "NNP", "NNPS"]:
            ent = ent + w.text + " "

    ent = ent.strip()

    return [QueryType.ENTITY]


# Getting the words of a specific dependancy (incl. all the compounds in front of it)
def get_word_by_dep(words, dep_list, dep):
    result = None
    for idx in range(len(dep_list)):
        if dep_list[idx] == dep:
            result = words[idx]
        if result:
            break
    if not result:
        pass
        # print('Failed to retreive a ', dep)
    else:
        for x in range(idx):
            if dep_list[idx - (x + 1)] == "compound" or dep_list[idx - (x + 1 )] == "amod":
                result = words[idx - (x + 1)] + " " + result
            else:
                break
        # print(dep, " = ", result)
    return result


def get_words_and_dep(question, nlp):
    # nlp = spacy.load("en_core_web_sm")
    nlp.vocab["name"].is_stop = False
    tokens = []
    types = []
    parse = nlp(question.strip())
    for q in parse:
        tokens.append(q.text)
        types.append(q.dep_)
    return tokens, types
    # TODO
    # Create functions for extracting features.
    #
