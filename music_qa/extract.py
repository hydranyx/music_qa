from classifier import Question, QuestionType
import spacy

nlp_spacy = spacy.load('en')

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
	print(question)
	return ['prop', 'entity']

if __name__ == "__main__":
	nlp = spacy.load('en')
	question = Question('Who is the father of Miley Cyrus?', nlp)
	extract_feautures(question, question.get_question_type())