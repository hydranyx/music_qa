from classifier import Question, QuestionType
import spacy

nlp_spacy = spacy.load('en')

def extract_features(question, question_type, nlp):
	nlp_spacy = nlp

	if question_type is QuestionType.BASE:
		result = base_question(question)
	elif question_type is QuestionType.LIST:
		result = list_question(question)
	elif question_type is QuestionType.BOOLEAN:
		result = boolean_question(question)
	elif question_type is QuestionType.COUNT:
		result = count_question(question)
	elif question_type is QuestionType.HIGHEST:
		result = highest_question(question)
	elif question_type is QuestionType.QUALIFIED:
		result = qualified_question(question)
	elif question_type is QuestionType.DESCRIPTION:
		result = description_question(question)
	return result

def base_question(question):
	#print(question)
	return ['prop', 'entity']

def list_question(question):
	result = nlp_spacy(question.question)
		
	entities = []
	properties = []

	# Search for entities
	for ent in result.ents:
		entities.append(ent.text)

	# Search for properties
	for sent in result.sents:
		for token in sent:
			if token.dep_ == 'nsubj' and token.ent_type_ is '':
				for x in token.subtree:
					if x.pos_ == 'NOUN' or x.pos_ == 'ADJ' and x.ent_type_ is '':
						properties.append(x.text)
				properties.append(token.text)
			elif token.dep_ == 'attr' and token.ent_type_ is '':
				for x in token.subtree:
					if x.pos_ == 'NOUN' or x.pos_ == 'ADJ' and x.ent_type_ is '':
						properties.append(x.text)
				properties.append(token.text)
			elif token.dep_ == 'nsubjpass' and token.ent_type_ is '':
				for x in token.subtree:
					if x.pos_ == 'NOUN' or x.pos_ == 'ADJ' and x.ent_type_ is '':
						properties.append(x.text)
				properties.append(token.text)
			if token.dep_ == 'advmod' and token.ent_type_ is '':
				for x in token.subtree:
					if x.pos_ == 'NOUN' or x.pos_ == 'ADJ' and x.ent_type_ is '':
						properties.append(x.text)
				properties.append(token.text)
			if token.dep_ == 'dobj' and token.ent_type_ is '':
				for x in token.subtree:
					if x.pos_ == 'NOUN' or x.pos_ == 'ADJ' and x.ent_type_ is '':
						properties.append(x.text)
				properties.append(token.text)

	# Remove entities from the properties
	used = set(entities)
	properties = [x for x in properties if x not in used and (used.add(x) or True)]
	for item in ['What', 'When', 'Who']:
		if item in properties:
			properties.remove(item)
	
	prop = " ".join(properties)

	if prop == '' or len(entities) == 0:

		question.question_type = QuestionType.DESCRIPTION
		description_question(question)

	return [prop, entities]

def boolean_question(question):
	#print(question)

	#Getting the individual words, and the dependencies
	words, dep_list = get_words_and_dep(question.question)

    #Try to get an entity 
	ent = get_word_by_dep(words, dep_list, 'nsubj')

    ##If there is an entity, try to get a attribute
	if ent:
		attr = get_word_by_dep(words, dep_list, 'attr')

		#If there is no attr, often the dobj is the attribute
		if not attr:
			attr = get_word_by_dep(words, dep_list, 'dobj')
		
		if not attr:
			attr = get_word_by_dep(words, dep_list, 'pobj')

		#If this is also not the case, often the verb/root is the attribute
		if not attr:
			attr = get_word_by_dep(words, dep_list, 'ROOT')

	#If there is no entity, often the ROOT is the entity and dobj the attribute (e.g. Is rapping a music style?)
	else:
		ent = get_word_by_dep(words, dep_list, 'ROOT')
		attr = get_word_by_dep(words, dep_list, 'dobj')
	#TODO a boolean question has another pair of words (not a prop, but a attr)
	return [attr, ent]

def count_question(question):
	#print(question)
	return ['prop', 'entity']

def highest_question(question):

	words, dep_list = get_words_and_dep(question.question)

	prop = get_word_by_dep(words, dep_list, 'amod') + ' ' + get_word_by_dep(words, dep_list, 'nsubj')

	ent = get_word_by_dep(words, dep_list, 'pobj')

	ent.strip()
	prop.strip()

	return [prop, ent]

def qualified_question(question):
	print(question)
	return ['prop', 'entity']

def description_question(question):
	
	parse = nlp_spacy(question.question)

	prop = ''
	ent = ''

	for w in parse:
		if w.tag_ in ['NN','NNS','NNP','NNPS']:
			ent = ent + w.text + ' '

	ent = ent.strip()

	return {'property': prop, 'entity': [ent]}

#Getting the words of a specific dependancy (incl. all the compounds in front of it)
def get_word_by_dep(words, dep_list, dep):
	result = None
	for idx in range(len(dep_list)):
		if dep_list[idx] == dep:
			result = words[idx]
		if result:        
			break
	if not result:
		pass
		#print('Failed to retreive a ', dep)
	else:
		for x in range(idx):
			if dep_list[idx-(x+1)] == 'compound':
				result = words[idx-(x+1)] + ' ' + result
			else:
				break
		#print(dep, " = ", result)
	return result

def get_words_and_dep(question):
    #nlp = spacy.load("en_core_web_sm")
    nlp_spacy.vocab["name"].is_stop = False
    tokens = []
    types = []
    parse = nlp_spacy(question.strip())
    for q in parse:
        tokens.append(q.text)
        types.append(q.dep_)
    return tokens, types

if __name__ == "__main__":
	nlp = spacy.load('en')

	question = Question('What bands did Kurt Cobain play in?', nlp)
	question.question_type = QuestionType.LIST
	print(extract_features(question, question.get_question_type(), nlp))