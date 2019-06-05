def get_dictionary():
	''' Add item to dictionary by using key followed by a list of items that are synonyms
		EXAMPLE: "birth name": ['real name', 'given name']
	'''
    dictionary = {"birth name": ["real name", "given name"],
     "occupation": ["play on", "job"]}

     return dictionary

def get_dictionary_synonym(prop):
	dictionary = get_dictionary()
	return dictionary[prop]

