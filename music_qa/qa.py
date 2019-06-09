"""
The QA system which way may be queried for answers.
"""

import logging
from .answer import Answer
from .extractor import Extractor


class Qa:
    """ The Qa maintains the infrastructure for answering questions. It may be
    queried to answer some question and result in an answer. """

    def __init__(self):
        logging.info("Starting QA system")
        self.extractor = Extractor()

    def answer(self, question):
        """ Answer the provided question if possible. """
        logging.debug("Answering: %s", question)
        logging.debug("Preparing: %s", question)
        question = self.extractor.prepare_question(question)
        print(question.features)
        logging.debug("Executing query for question: %s", question)
        answer = question.execute()
        return Answer(answer)
