"""
Thesaurus-like lookup for phrases.
"""


def entity_special_case(phrase):
    return phrase


def property_special_case(phrase):
    if "country" in phrase:
        return "country of origin"
    if phrase == "die":
        return "death"
    if phrase == "born":
        return "birth"
    if phrase == "buried":
        return "burial"
    if "member" in phrase:
        return "has part"
    if phrase == "invent":
        return "inventor"
    if phrase == "sing":
        return "perform"
    if phrase == "found":
        return "founder"
    if phrase == "compose":
        return "composer"
    return phrase


class Thesaurus:
    """ A thesaurus class, allowing for synonym lookup. """

    def __init__(self):
        self.thesaurus = [
            {"birth name", "real name", "given name"},  # <-- how it is now
            {"occupation", "play on", "job"},
        ]

        self.thasaurus = {
            "originated": "country of origin",
            "originate": "country of origin",
            "originate in": "country of origin",
            "come from": "country of origin",
            "members": "has part",
            "member": "has part",
            "are in": "has part",
            "play in": "member of",
            "play": "member of",
            "band": "member of",
            "is in ": "member of",
            "music label": "record label",
            "written for": "part of",
            "also known as": "nickname",
            "also known as": "pseudonym",
            "known for": "notable work",
            "best known for": "notable work",
            "famous work": "notable work",
            "known work": "notable work",
            "famous for": "notable work",
            "best known work": "notable work",
            "play": "instrument",
            "start": "inception",
            "real name": "birth name",
            "given name": "birth name",
            "made": "has parts",
            "made of": "has parts",
            "main parts": "has parts",
            "look": "wears",
            "signature look": "wears",
            "instruments": "instrument",
            "sickness": "medical condition",
            "tempo": "beats per minute",
            "founder": "founded by",
            "year": "inception",
            "name": "birth name",
            "parts": "has part",
            "part": "has part", 
        }

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
