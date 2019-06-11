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
        logging.info("Preparing answer to: %s", question)
        question = self.extractor.prepare_question(question)
        if question:
            logging.info("Executing query for question")
            answer = question.execute()
            return Answer(answer)
        else:
            logging.info(
                "Question could not be classified. Try a different formulation?"
            )
            return Answer(None)
