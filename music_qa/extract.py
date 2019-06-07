from classifier import Question, QuestionType
import spacy

nlp_spacy = spacy.load('en_core_web_sm')

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
	print(question)
	return ['prop', 'entity']

def list_question(question):
	print(question)
	return ['prop', 'entity']

def boolean_question(question):
	print(question)

	#Getting the individual words, and the dependencies
	words, dep_list = get_words_and_dep(question.question)

    #Try to get an entity 
	ent = get_word_by_dep(words, dep_list, 'nsubj')

    #If there is an entity, try to get an attribute
	if ent:
		attr = get_word_by_dep(words, dep_list, 'attr')
		#If there is no attr, often the dobj is the attribute (TODO with compound?)
		if not attr:
			attr = get_word_by_dep(words, dep_list, 'dobj')
			if attr:
				pass

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
	print(question)
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
	
	parse = nlp(question.question)

	prop = ''
	ent = ''

	for w in parse:
		if w.tag_ in ['NN','NNS','NNP','NNPS']:
			ent = ent + w.text + ' '

	ent = ent.strip()

	return [prop, ent]

#Getting the words of a specific dependancy (incl. all the compounds in front of it)
def get_word_by_dep(words, dep_list, dep):
	result = None
	for idx in range(len(dep_list)):
		if dep_list[idx] == dep:
			result = words[idx]
		if result:        
			break
	if not result:
		print('Failed to retreive a ', dep)
	else:
		for x in range(idx):
			if dep_list[idx-(x+1)] == 'compound':
				result = words[idx-(x+1)] + ' ' + result
			else:
				break
		print(dep, " = ", result)
	return result

def get_words_and_dep(question):
    nlp = spacy.load("en_core_web_sm")
    nlp.vocab["name"].is_stop = False
    tokens = []
    types = []
    parse = nlp(question.strip())
    for q in parse:
        tokens.append(q.text)
        types.append(q.dep_)
    return tokens, types

if __name__ == "__main__":
	nlp = spacy.load('en_core_web_sm')
	question = Question('Who is Eminem?', nlp)
	question.question_type = QuestionType.DESCRIPTION
	extract_features(question, question.get_question_type(), nlp)