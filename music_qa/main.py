from classifier import Question, QuestionType
from extract import extract_features
from get_wikidata import get_wikidata
from fire_query import fire_query
import spacy

def main():
	nlp = spacy.load('en')

	for line in open("test_boolean_questions.txt"):
		splitted = line.split("\t")
		
		# Get Question and type
		question = Question(splitted[-1], nlp)
		question.determine_type()
		question_type = question.get_question_type()
		features = extract_features(question, question_type, nlp) # Return List with Entities and Properties
		
		#features[0] is Entity, features[1] is property"
		#TODO: Add function to check dictionary here. 
		print('type 1: ', features)
		print('type 2: ', features[0])
		ent_value = get_wikidata(features[0], 'entity')
		prop_value = get_wikidata(features[1], 'property')

		answer = fire_query(ent_value, prop_value, question_type)
		
		print(answer)

if __name__ == '__main__':
	main()