from classifier import Question, QuestionType
from extract_features import extract_features
import spacy

def main():
	#Import Spacy
	nlp = spacy.load('en')

	for line in open("all_questions.txt"):
		splitted = line.split("\t")
		question = Question(splitted[-1], nlp)
		
		print(question.get_question_type())

		prop, entity = extract_features(question_type)
		prop_num, entity_num = extract_features_wikidata(question_type)
		
		answer = fire_query(prop, entity, question_type)



if __name__ == '__main__':
	main()