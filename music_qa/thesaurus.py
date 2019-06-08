"""
Thesaurus-like lookup for phrases.
"""


class Thesaurus:
    """ A thesaurus class, allowing for synonym lookup. """

    def __init__(self):
        self.thesaurus = [
            {"birth name", "real name", "given name"},
            {"occupation", "play on", "job"},
        ]

    def add_synonyms(self, synonym_set):
        """ Add a set of synonyms to the thesaurus. """
        self.thesaurus.append(synonym_set)

    def get_synonyms(self, phrase):
        """ Get the list of synonyms for a phrase. If the phrase does not
        exist in the thesaurus, then the result is an empty list. """

        # Find the first set of phrases associated with the provided
        # phrase.

        synonyms = next(filter(lambda synonyms: phrase in synonyms, self.thesaurus), {})

        # Remove the provided phrase from the set
        synonyms.discard(phrase)

        return list(synonyms)
