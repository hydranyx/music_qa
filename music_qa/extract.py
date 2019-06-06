from classifier import Question, QuestionType
import spacy

nlp_spacy = spacy.load('en_core_web_sm')

def extract_features(question, question_type, nlp):
	nlp_spacy = nlp

	if question_type is QuestionType.BASE:
		base_question(question)
	elif question_type is QuestionType.LIST:
		list_question(question)
	elif question_type is QuestionType.BOOLEAN:
		boolean_question(question)
	elif question_type is QuestionType.COUNT:
		count_question(question)
	elif question_type is QuestionType.HIGHEST:
		highest_question(question)
	elif question_type is QuestionType.QUALIFIED:
		qualified_question(question)
	elif question_type is QuestionType.DESCRIPTION:
		description_question(question)

def base_question(question):
	print(question)
	return ['prop', 'entity']

def list_question(question):
	print(question)
	return ['prop', 'entity']

def boolean_question(question):
	print(question)
	return ['prop', 'entity']

def count_question(question):
	print(question)
	return ['prop', 'entity']

def highest_question(question):
	print(question)
	return ['prop', 'entity']

def qualified_question(question):
	print(question)
	return ['prop', 'entity']

def description_question(question):
	
	parse = nlp(question.question)

	prop = ''
	entity = ''

	for w in parse:
		if w.tag_ in ['NN','NNS','NNP','NNPS']:
			entity = entity + w.text + ' '

	entity = entity.rstrip()

	print('entity: ' + entity + ' property: ' + prop)

	return ['prop', 'entity']

def get_word_by_dep(words, dep_list, dep):
    result = None
    for idx in range(len(dep_list)):
        if dep_list[idx] == dep:
            result = words[idx]
    if result:        
        print(dep, " = ", result)
    else:
        print('Failed to retreive a ', dep)
    return result

if __name__ == "__main__":
	nlp = spacy.load('en_core_web_sm')
	question = Question('Who is Eminem?', nlp)
	question.question_type = QuestionType.DESCRIPTION
	extract_features(question, question.get_question_type(), nlp)