import re
from .wikidata_mapper import QueryType
from .question import QuestionType
import spacy


class Classifier:
    def __init__(self):
        self.nlp = spacy.load("en")

    def classify(self, question):
        doc = self.nlp(question)

        # HIGHEST Question
        m = re.search(
            "(?:highest|lowest|first|last|oldest|youngest|earliest|latest|smallest|biggest|greatest|newest)",
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
        # TODO make sure that this is description only if either property or entity are present but not both.
        m = re.fullmatch(
            "(What|Who) (is|are|were|was) (the )?([^(\?|of)]*)( ?\?)?",
            question,
            re.IGNORECASE,
        )
        print(m)
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
