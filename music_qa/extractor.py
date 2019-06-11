"""
The extractor handles extracting the correct details from a string and turning
it into a question. THe question may then be executed to determine its answer,
if it has one.
"""

import logging
import spacy
from .classifier import Classifier


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en")
        self.classifier = Classifier()

    def prepare_question(self, question):
        # Normalize question by lowercasing and lemmatizing it
        question = self.normalize_question(question)
        logging.info("Normalizing question to '%s'", question)
        question = self.classifier.classify(question)
        logging.info("Classifying question as %s", type(question))
        return question

    def normalize_question(self, question):
        """
        Return the normalized form of the provided question.
        The aim is for this to be idempotent.
        """

        normal_form = ""
        for token in self.nlp(question):
            # Exclude unneeded tokens such as extraneous spaces or punctuation.
            if token.pos_ in ["PUNCT", "SPACE"]:
                continue
            else:
                # If the token is not a possessive ending add a space
                if (token.tag_, token.pos_) != ("POS", "PART"):
                    normal_form += " "

                if token.text.lower() == "born":
                    # Special case: {BORN}
                    # The default spaCy lemmatizer treats the lemma as "bear"
                    lemma = "born"
                elif token.text.lower() == "buried":
                    lemma = "buried"
                elif token.text == "Queen":
                    # Special case: Queen
                    # As our system is specialized for Music queries we should consider the lemma of Queen to be "queen".
                    lemma = "Queen"
                elif token.text == "Rhapsody":
                    # Special case: Bohemian Rhapsody
                    # spaCy's entity detector is used here, it can't detect this when correctly spelled (when using "en_core_web_sm")
                    # So we misspell it (which it can detect correctly)
                    lemma = "Rapsody"
                elif token.dep_ == "amod":
                    lemma = token.text.lower()
                else:
                    lemma = token.lemma_
                    if lemma == "-PRON-":
                        lemma = token.text.lower()

                normal_form += lemma

        normal_form = normal_form.strip()

        normal_form = normal_form.strip()
        return normal_form
