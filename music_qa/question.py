"""
A question as interpreted by the QA system.
"""

import logging
import random
import spacy
import itertools
from enum import Enum
from music_qa.wikidata_mapper import WikidataMapper, QueryType
from music_qa.wikidata_query import WikidataQuery
from abc import ABC, abstractmethod
import requests
from nltk.corpus import wordnet


# TODO don't reload the spacy model
NLP = spacy.load("en")


class QuestionType(Enum):
    BOOLEAN = 1
    COUNT = 2
    DESCRIPTION = 3
    HIGHEST = 4
    LIST = 5
    QUALIFIED = 6


class Question(ABC):
    """
    A base question as used by the QA system.
    """

    def __init__(self, question):
        self.wikidata_query = WikidataQuery()
        self.question = question

    def __str__(self):
        return "Question: " + self.question

    @abstractmethod
    def primary_strategy(self):
        pass

    def fallback_strategy(self):
        return None

    def add_features(self, features):
        self.features = features

    def get_wikidata(self, text, use):
        url = "https://www.wikidata.org/w/api.php"
        params = {"action": "wbsearchentities", "language": "en", "format": "json"}
        info = []

        if use == "entity":
            params["type"] = "item"
            pass
        elif use == "property":
            params["type"] = "property"
        else:
            print(
                "uncorrect call, specify type of info(entity/property) as second argument"
            )
            return info

        words = []
        words.append(text)
        synonyms = []

        for word in words:
            params["search"] = word
            json = requests.get(url, params).json()
            for result in json["search"]:
                info.append(result["id"])
            if info:
                break
            if not synonyms:
                synonyms = wordnet.synsets(text)
                for synonym in synonyms:
                    a = synonym.lemmas()[0].name()
                    b = a.replace("_", " ")
                    words.append(b)
        return info

    def execute(self):
        result = self.primary_strategy()
        if result is None:
            result = self.fallback_strategy()
        return result


class BooleanQuestion(Question):
    def __init__(self, question):
        super(BooleanQuestion, self).__init__(question)
        # NOTE to add parameters after constructing the super class: do.
        # self.parameter_name = whatever argument

    def primary_strategy(self):
        #TODO fire specific query with entity and attribute
        q_number = self.get_wikidata(self.features['entity'], 'entity')
        print('BooleanQuestion: Primary strategy not correctly implemented yet ')
        answer = self.wikidata_query.list_type1_q(q_number[0], self.features['attribute'])
        return (answer['results']['bindings'][0]['itemLabel']['value'] == self.features['attribute'])

    def fallback_strategy(self):
        return random.choice([True, False])


class ListQuestion(Question):
    def __init__(self, question, property, entity):
        super(ListQuestion, self).__init__(question)
        self.mapper = WikidataMapper()
        self.property = property
        self.entity = entity

    def primary_strategy(self):
        print(self.property, self.entity)
        return None

    def secundary_strategy(self):
        return None


class CountQuestion(Question):
    def __init__(self, question):
        super(CountQuestion, self).__init__(question)

    def primary_strategy(self):
        return None


class HighestQuestion(Question):
    def __init__(self, question):
        super(HighestQuestion, self).__init__(question)

    def primary_strategy(self):
        return None


class QualifiedQuestion(Question):
    def __init__(self, question):
        super(QualifiedQuestion, self).__init__(question)

    def primary_strategy(self):
        return None


class DescriptiveQuestion(Question):
    def __init__(self, question, descriptive_type):
        super(DescriptiveQuestion, self).__init__(question)
        self.mapper = WikidataMapper()
        self.descriptive_type = descriptive_type

    def primary_strategy(self):
        return None

    def primary_strategy(self):
        if self.descriptive_type == QueryType.ENTITY:
            item = extract_entity(self.question)
        elif self.descriptive_type == QueryType.PROPERTY:
            item = extract_property(self.question)
            pass

        mapping = self.mapper.get_closest_map(item, self.descriptive_type)

        if mapping is None:
            return None

        label = mapping["label"]
        description = mapping["description"]
        return "{}: {}".format(label, description)

    def fallback_strategy(self):
        # Call thesaurus on the entity/ property and then rerun the same logic
        # as primary again and again, until not None or no possibilities left.
        pass


## TODO move to different location.
## DON'T TOUCH WHILE THE OTHER QUESTIONS ARE STILL BEING BUILT.
def extract_entity(question):
    """ Extracts the entity from a question. """

    # Prepare the document
    doc = NLP(question)
    # Extract index of the POS tag
    index = None
    ents = None
    for token in doc:
        if token.tag_ == "POS":
            index = token.i
            break
    if index:
        # make a sub string and extract its entity
        sub_doc = NLP(str(doc[:index]))
        ents = sub_doc.ents

    # If there are no entities
    if not ents:
        # Extract entities using Spacy
        ents = doc.ents

    # if there are still no entities
    if not ents:
        # consider object nouns
        ents = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == "pobj"]

    # if there are still no entities
    if not ents:
        # consider object nouns
        ents = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == "nsubj"]

    if not ents:
        ents = [
            NLP(token.text)[:]
            for token in doc
            if token.tag_ in ["NN", "NNS", "NNP", "NNPS"]
        ]

    # Extract the last entity
    entity = ents[-1]

    # If the entity is a compound
    # TODO this should be generalized
    if entity.root.dep_ == "conj":
        # Combine text
        entity = ents[-2].text + " and " + ents[-1].text
    else:
        subdoc = NLP(entity.text)
        # Recombine the words
        entity = " ".join(
            list(
                map(
                    # Convert to text
                    lambda token: token.lemma_,
                    # Remove leading stop words
                    itertools.dropwhile(
                        lambda token: token.text in ["a", "an"], subdoc
                    ),
                )
            )
        )

    return entity


def extract_property(question):
    """ Extracts the property from a question. """

    # Extract the entity to simply property extraction
    entity = extract_entity(question)
    # Remove the entity from the question
    idx = question.rfind(entity)
    question = question[:idx] + question[idx + len(entity) :]

    # Prepare the document
    doc = NLP(question)

    # Extract the possible properties
    property_span = [
        chunk for chunk in doc.noun_chunks if chunk.root.tag_ in ["NN", "NNS"]
    ]

    if not property_span:
        doc = NLP(question[idx:].strip())
        property_span = [token for token in doc]
        if property_span:
            return property_span[0].text

    # Assert that the question is not empty
    # TODO consider error handling
    assert question

    # If there is one property
    if len(property_span) == 1:
        # Set that property
        property = property_span[0]
    else:
        # Combine the property span
        property = doc[property_span[0].start : property_span[-1].end]

    # Recombine the words
    property = " ".join(
        list(
            map(
                # Convert to text
                lambda token: token.lemma_,
                # Remove leading stop words
                itertools.dropwhile(lambda token: token.is_stop, property),
            )
        )
    )

    return property
