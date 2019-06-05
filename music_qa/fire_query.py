def fire_query(entity, prop, question_type):
	"""Send a request to the wikidata API and returns the results. """
	if question_type is QuestionType.BASE:
		query = 'SELECT ?xLabel WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)
	elif question_type is QuestionType.LIST:
		query = 'SELECT ?xLabel WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)
	elif question_type is QuestionType.BOOLEAN:
		query = 'SELECT ?xLabel WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)
	elif question_type is QuestionType.COUNT:
		query = 'SELECT (COUNT(*) AS ?count) WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)
	elif question_type is QuestionType.HIGHEST:
		query = 'SELECT ?xLabel WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)
	elif question_type is QuestionType.QUALIFIED:
		query = 'SELECT ?xLabel WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)
	elif question_type is QuestionType.DESCRIPTION:
		query = 'SELECT ?xLabel WHERE {{  wd:{} wdt:{} ?x . SERVICE wikibase:label {{    bd:serviceParam wikibase:language "en" .  }}}}'.format(entity, prop)

	data = requests.get(url,params={'query': query, 'format': 'json'}).json()
	results = []
	if len(data['results']['bindings']) != 0:
		for item in data['results']['bindings']:
			for var in item:
				results.append(item[var]['value'])
		return results