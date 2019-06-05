"""
TODO Module documentation.
"""
import itertools
import sys
import spacy

NLP = spacy.load("en_core_web_sm")
NLP.vocab["name"].is_stop = False

API_URL = "https://www.wikidata.org/w/api.php"
SPARQL_URL = "https://query.wikidata.org/sparql"


def extract_item(question):


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

    # Extract the last entity
    entity = ents[-1]

    # If the entity is a compound
    # TODO this should be generalized
    if entity.root.dep_ == "conj":
        # Combine text
        entity = ents[-2].text + " and " + ents[-1].text
    else:
        # Extract text
        entity = entity.text

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


def extract_features(question):
    """ Extracts the features needed to (attempt to) answer a question. """
    return extract_property(question), extract_entity(question)


def get_question_type(question):

    # Try to extract the needed features from the string
    try:
        print("See what can be extracted and what gets extracted.")
        # What does the question have, structuray and feature wise?
        property
    except ValueError as err:
        print(err)

    return question_type
