from enum import Enum
import re
import spacy


class QuestionType(Enum):
	BASE		= 0
	LIST 		= 1
	BOOLEAN 	= 2
	COUNT 		= 3
	HIGHEST 	= 4
	QUALIFIED 	= 5
	DESCRIPTION = 6


class Question:
	def __init__(self, question, nlp):
		self.question = question
		self.question_type = QuestionType.BASE
		self.nlp = nlp
		self.determine_type()
	
	def determine_type(self):
		result = self.nlp(self.question)
		entities = []

		# HIGHEST Question
		m = re.search('(?:highest|lowest|first|last|oldest|youngest|earliest|latest)', self.question, re.IGNORECASE)
		if m is not None  and self.question_type is QuestionType.BASE:
			self.question_type = QuestionType.HIGHEST

		# BOOLEAN Question
		if result[0].tag_[0] == 'V' and self.question_type is QuestionType.BASE:
			self.question_type = QuestionType.BOOLEAN

		# COUNT Question
		m = re.search('(?:How) (?:many|much)', self.question, re.IGNORECASE)
		if m is not None  and self.question_type is QuestionType.BASE:
			self.question_type = QuestionType.COUNT		

		# DESCRIPTION Question
		# TODO IN LIST

		# LIST Question
		m = re.search('(?:What|Who|Where|When)', self.question, re.IGNORECASE)
		m2 = re.search('(?:In) (?:What|Which)', self.question, re.IGNORECASE)
		m3 = re.search('(?:Which)', self.question, re.IGNORECASE)
		m4 = re.search('(?:How did)', self.question, re.IGNORECASE)
		if self.question_type == QuestionType.BASE:
			if m is not None or m2 is not None or m3 is not None or m4 is not None:
				self.question_type = QuestionType.LIST		

		if self.question_type == QuestionType.BASE:
			return False
		else:
			return True

	def get_question_type(self):
		return self.question_type

	def get_question(self):
		return self.question
		
if __name__ == '__main__':
	all_questions = []
	nlp = spacy.load('en')
	total_questions = 0
	matches = 0
	for line in open("all_questions.txt"):
		total_questions += 1
		splitted = line.split("\t")
		question = Question(splitted[-1], nlp)
		if question.determine_type():
			matches += 1
		all_questions.append(question)

	file_name = 'output.txt'
	file = open(file_name, 'w')

	for question in all_questions:
		file.write("{0:30} ".format(question.question_type) + question.question)

	file.close()


	print(str(matches) + "/" + str(total_questions))
	
