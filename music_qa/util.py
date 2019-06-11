import spacy
import itertools
import logging


# TODO don't reload the spacy model
NLP = spacy.load("en")
NLP.vocab["name"].is_stop = False


def extract_entity(question):
    """ Extracts the entity from a question. """
    # Prepare the document
    doc = NLP(question)
    # Extract index of the POS tag
    index = None
    ents = None
    for token in doc:
        if (token.tag_, token.pos_) == ("POS", "PART"):
            index = token.i
            break
    if index:
        # make a sub string and extract its entity
        sub_doc = NLP(str(doc[:index]))
        ents = sub_doc.ents

    if not ents:
        for np in list(doc.ents):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
        # Extract entities using Spacy
        ents = doc.ents

    # if there are still no entities
    if not ents:
        # consider object nouns
        for np in list(doc.noun_chunks):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
        ents = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == "pobj"]
    # If there are no entities

    if not ents:
        ents = [
            NLP(token.text)[:]
            for token in doc
            if token.tag_ in ["NN", "NNS", "NNP", "NNPS"]
        ]

    # if there are still no entities
    if not ents:
        # consider object nouns
        for np in list(doc.noun_chunks):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
        ents = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == "nsubj"]

    if not ents:
        return None

    # Extract the last entity
    entity = ents[-1]

    if len(entity) == 1 and entity[0].tag_ == "WP":
        return None

    # If the entity is a compound
    # TODO this should be generalized
    if entity.root.dep_ == "conj":
        # Combine text
        entity = ents[-2].text + " and " + ents[-1].text
    else:
        subdoc = NLP(entity.text)
        # Recombine the words
        entity = " ".join(
            list(
                map(
                    # Convert to text
                    lambda token: token.text,
                    # Remove leading stop words
                    itertools.dropwhile(
                        lambda token: token.text in ["a", "an", "the"], subdoc
                    ),
                )
            )
        )

    return entity


def extract_property(question):
    """ Extracts the property from a question. """
    # Extract the entity to simplify property extraction
    entity = extract_entity(question)

    # Prepare the document
    doc = NLP(question)
    entity_number = next((token.i for token in doc if token.text == entity), None)

    if entity_number:
        # one thing left after the entity
        if len(doc) == entity_number + 2:
            if doc[entity_number + 1].pos_ == "VERB":
                return doc[entity_number + 1].text

    if entity:
        # Remove the entity from the question
        idx = question.rfind(entity)
        if question[idx + len(entity) : idx + len(entity) + 2] == "'s":
            question = question[:idx] + question[idx + len(entity) + 2 :]
        else:
            question = question[:idx] + question[idx + len(entity) :]

    # Prepare the document
    doc = NLP(question)

    filtered = [token for token in doc if not token.is_stop]

    if filtered:
        if len(filtered) == 1:
            return filtered[0].text

    # Extract the possible properties
    property_span = [
        chunk for chunk in doc.noun_chunks if chunk.root.tag_ in ["NN", "NNS"]
    ]

    if entity and not property_span:
        doc = NLP(question[idx:].strip())
        property_span = [token for token in doc]
        if property_span:
            return property_span[0].text

    if not question:
        return None

    # If there is no property
    if not property_span:
        return None

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
                lambda token: token.text,
                # Remove leading det workds
                itertools.dropwhile(lambda token: token.pos_ == "DET", property),
            )
        )
    )

    return property


# Getting the words of a specific dependancy (incl. all the compounds in front of it)
def get_word_by_dep(words, dep_list, dep):
    result = None
    for idx in range(len(dep_list)):
        if dep_list[idx] == dep:
            result = words[idx]
        if result:
            break
    if not result:
        pass
    else:
        for x in range(idx):
            if (
                dep_list[idx - (x + 1)] == "compound"
                or dep_list[idx - (x + 1)] == "amod"
            ):
                result = words[idx - (x + 1)] + " " + result
            else:
                break
    return result


def get_words_and_dep(question, nlp):
    # NLP.vocab["name"].is_stop = False
    tokens = []
    types = []
    doc = nlp(question.strip())
    for q in doc:
        tokens.append(q.text)
        types.append(q.dep_)
    return tokens, types


def extract_entity_boolean(question):
    """ Extracts the entity from a question. """
    # Prepare the document
    doc = NLP(question)
    # Extract index of the POS tag
    index = None
    ents = None
    for token in doc:
        if (token.tag_, token.pos_) == ("POS", "PART"):
            index = token.i
            break
    if index:
        # make a sub string and extract its entity
        sub_doc = NLP(str(doc[:index]))
        ents = sub_doc.ents

    if not ents:
        for np in list(doc.ents):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
        # Extract entities using Spacy
        ents = doc.ents

    # if there are still no entities
    if not ents:
        # consider object nouns
        for np in list(doc.noun_chunks):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
        ents = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == "pobj"]
    # If there are no entities

    if not ents:
        ents = [
            NLP(token.text)[:]
            for token in doc
            if token.tag_ in ["NN", "NNS", "NNP", "NNPS"]
        ]

    # if there are still no entities
    if not ents:
        # consider object nouns
        for np in list(doc.noun_chunks):
            np.merge(tag=np.root.tag_, lemma=np.root.lemma_, ent_type=np.root.ent_type_)
        ents = [chunk for chunk in doc.noun_chunks if chunk.root.dep_ == "nsubj"]

    if not ents:
        return None

    # Extract the last entity
    entity = ents[0]

    if len(entity) == 1 and entity[0].tag_ == "WP":
        return None

    # If the entity is a compound
    # TODO this should be generalized
    if entity.root.dep_ == "conj":
        # Combine text
        entity = ents[-2].text + " and " + ents[-1].text
    else:
        subdoc = NLP(entity.text)
        # Recombine the words
        entity = " ".join(
            list(
                map(
                    # Convert to text
                    lambda token: token.text,
                    # Remove leading stop words
                    itertools.dropwhile(
                        lambda token: token.text in ["a", "an", "the"], subdoc
                    ),
                )
            )
        )

    return entity


def extract_property_boolean(question):
    """ Extracts the property from a question. """
    # Extract the entity to simplify property extraction
    entity = extract_entity_boolean(question)

    # Prepare the document
    doc = NLP(question)

    entity_number = next((token.i for token in doc if token.text == entity), None)
    if entity_number:
        # one thing left after the entity
        if len(doc) == entity_number + 2:
            if doc[entity_number + 1].pos_ == "VERB":
                return doc[entity_number + 1].text

    if entity:
        # Remove the entity from the question
        idx = question.rfind(entity)
        if question[idx + len(entity) : idx + len(entity) + 2] == "'s":
            question = question[:idx] + question[idx + len(entity) + 2 :]
        else:
            question = question[:idx] + question[idx + len(entity) :]

    # Prepare the document
    doc = NLP(question)

    filtered = [token for token in doc if not token.is_stop]

    if filtered:
        if len(filtered) == 1:
            return filtered[0].text

    # Extract the possible properties
    property_span = [
        chunk for chunk in doc.noun_chunks if chunk.root.tag_ in ["NN", "NNS"]
    ]

    if entity and not property_span:
        doc = NLP(question[idx:].strip())
        property_span = [token for token in doc]
        if property_span:
            return property_span[0].text

    if not question:
        return None

    # If there is no property
    if not property_span:
        return None

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
                lambda token: token.text,
                # Remove leading det workds
                itertools.dropwhile(lambda token: token.pos_ == "DET", property),
            )
        )
    )

    return property
