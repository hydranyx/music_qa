"""
Thesaurus-like lookup for phrases.
"""


def entity_special_case(phrase):
    return phrase


def property_special_case(phrase):
    if "country" in phrase:
        return "country of origin"
    if "member" in phrase:
        return "has part"

    thasaurus = Thesaurus().thasaurus
    for key in thasaurus:
        if phrase == key:
            return thasaurus[key]

    return phrase


class Thesaurus:
    """ A thesaurus class, allowing for synonym lookup. """

    def __init__(self):
        self.thesaurus = [
            {"birth name", "real name", "given name"},  # <-- how it is now
            {"occupation", "play on", "job"},
        ]

        self.thasaurus = {
            "die": "death",
            "born": "birth",
            "buried": "burial",
            "invent": "inventor",
            "compose": "composer",
            "sing": "perform",
            "found": "founder",
            "originated": "country of origin",
            "originate": "country of origin",
            "originate in": "country of origin",
            "come": "country of origin",
            "members": "has part",
            "member": "has part",
            "are in": "has part",
            "play in": "member of",
            "play": "member of",
            "band member": "member of",
            "band": "part of",
            "is in ": "member of",
            "music label": "record label",
            "kid": "child",
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
