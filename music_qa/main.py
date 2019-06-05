from classifier import Question, QuestionType
from extract import extract_features
from get_wikidata import get_wikidata
import spacy

def main():
	#Import Spacy
	nlp = spacy.load('en')

	for line in open("all_questions.txt"):
		splitted = line.split("\t")
		
		# Get Question and type
		question = Question(splitted[-1], nlp)
		question.determine_type()
		question_type = question.get_question_type()
		features = extract_features(question, question_type, nlp)
		
		#prop_value = get_wikidata(question, 'property')
		#ent_value = get_wikidata(question, 'entity')
		
		#answer = fire_query(prop, entity, question_type)

if __name__ == '__main__':
	main()