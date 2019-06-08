import re
from .wikidata_mapper import QueryType
from .question import QuestionType
import spacy


class Classifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def classify(self, question):
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
