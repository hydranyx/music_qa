"""
The classifier determines if a question should be of a particular type.
"""
import spacy
import logging
import re
from .util import (
    extract_entity,
    extract_property,
    get_words_and_dep,
    get_word_by_dep,
    extract_entity_boolean,
    extract_property_boolean,
)
from .questions import (
    BooleanOnlyQuestion,
    BooleanQuestion,
    CountQuestion,
    DescribeEntityQuestion,
    DescribePropertyQuestion,
    HighestQuestion,
    XofYHowQuestion,
    XofYQuestion,
    XofYWhatQuestion,
    XofYWhenQuestion,
    XofYWhereQuestion,
    XofYWhoQuestion,
)


class Classifier:
    def __init__(self):
        self.nlp = spacy.load("en")

    def classify(self, question):
        doc = self.nlp(question)

        for classifier in [
            self.classify_descriptive_question,
            self.classify_count_question,
            self.classify_boolean_question,
            # TODO highest doesn't work yet and breaks things which have a valid property like "highest note"
            # self.classify_highest_question,
            # X of Y is the most generic and should be kept at the bottom.
            self.classify_x_of_y_question,
        ]:
            classified_question = classifier(question)
            if classified_question:
                return classified_question

        # TODO decide between these two
        return None
        # raise RuntimeError("Question {} could not be classified".format(question))

    def classify_descriptive_question(self, question):
        doc = self.nlp(question)

        elem = next(
            (
                token
                for token in doc
                if token.text in ["what", "who"] and token.tag_ == "WP"
            ),
            None,
        )
        if elem:
            entity = extract_entity(question)
            property = extract_property(question)

            if property is None and entity:
                return DescribeEntityQuestion(question, entity)

            if property and entity is None:
                return DescribePropertyQuestion(question, property)
        return None

    def classify_count_question(self, question):
        doc = self.nlp(question)
        matches = re.search("(how many)|(how much)", question)
        if matches:
            start, end = matches.span()
            sub_question = (question[:start] + question[end:]).strip()
            entity = extract_entity(sub_question)
            property = extract_property(sub_question)
            logging.info("(entity, property) = %s", (entity, property))
            if entity and property:
                return CountQuestion(question)
        return None

    def classify_x_of_y_question(self, question):
        doc = self.nlp(question)
        elem = next(
            (
                token
                for token in doc
                if (token.text, token.tag_)
                in [
                    ("who", "WP"),
                    ("what", "WP"),
                    ("when", "WRB"),
                    ("where", "WRB"),
                    ("how", "WRB"),
                ]
            ),
            None,
        )
        entity = extract_entity(question)
        property = extract_property(question)
        if property and entity:
            logging.info("(entity, property) = %s", (entity, property))
            if not elem:
                return XofYQuestion(question, entity, property)
            elif elem.text == "who":
                return XofYWhoQuestion(question, entity, property)
            elif elem.text == "what":
                return XofYWhatQuestion(question, entity, property)
            elif elem.text == "when":
                return XofYWhenQuestion(question, entity, property)
            elif elem.text == "where":
                return XofYWhereQuestion(question, entity, property)
            elif elem.text == "how":
                return XofYHowQuestion(question, entity, property)
        return None

    def classify_boolean_question(self, question):
        doc = self.nlp(question)

        if doc[0].tag_[0] == "V":
            # Extract features
            # Getting the individual words, and the dependencies
            words, dep_list = get_words_and_dep(question, self.nlp)
            logging.info("words %s deps dep_list %s", words, dep_list)

            # find either singular words like "only", "just", "uniquely", "exclusively", "solely"
            unique_indicator = next(
                filter(
                    lambda token: token.text
                    in ["only", "just", "uniquely", "exclusively", "solely"],
                    doc,
                ),
                None,
            )
            if unique_indicator:
                (indicator_start, indicator_end) = (
                    unique_indicator.idx,
                    unique_indicator.idx + len(unique_indicator.text),
                )
                # Remove the unique indicator to simplify extraction
                question = (
                    question[:indicator_start] + question[indicator_end + 1 :]
                ).strip()
                # Try to get an entity
                ent = extract_entity_boolean(question)
                attr = extract_property_boolean(question)
                logging.info(question)
                logging.info("(entity, attribute) = %s", (ent, attr))
                return BooleanOnlyQuestion(question, attr, ent)
            else:
                # Try to get an entity
                ent = extract_entity_boolean(question)
                attr = extract_property_boolean(question)
                logging.info("(entity, attribute) = %s", (ent, attr))
                return BooleanQuestion(question, attr, ent)

        return None

    def classify_highest_question(self, question):
        doc = self.nlp(question)
        amod_indicator = next(filter(lambda token: token.dep_ in ["amod"], doc), None)
        if amod_indicator:
            entity = extract_entity(question)
            property = extract_property(question)
            logging.info("(entity, property) = %s", (entity, property))
            return HighestQuestion(question, entity, property)

        return None
