import sys
import requests
import re
import spacy

#Printing and solving the example questions
def printExampleQueries():
    questions = [
        "What is the birth place of Bono?",
        "When was Bono born?",
        "What is the capital of France?",
        "Who is the president of France?",
        "When did Nelson Mandela die?",
        "When was Jamie Oliver born?",
        "What does a koala eat?",
        "Who is the mother of Beethoven?",
        "What is the website of Google?",
        "What is the king of the Netherlands?"
    ]
    for question in questions:
        print (question)
        solveQuestion (question)

def getSpacy(question, types):
    nlp = spacy.load('en')
    tokens = []
    for q in question.split() :
        parse = nlp(q.strip())
        for token in parse :
            # print("\t".join((token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.lemma_, token.ent_type_)))
            for type in types:
                if token.tag_ == type:
                    # print("found", token.text, "as", token.tag_)
                    tokens.append(token.text)
    return tokens
pass

#Obtain the Q/P numbers from WikiData
def getNumbers(name, params):
    url = "https://www.wikidata.org/w/api.php"
    params["search"] = name
    json = requests.get(url, params).json()
    numbers = []
    for result in json["search"]:
        numbers.append(result["id"])
    return numbers

#Remove the articles form the given string
def checkAndRemoveArticles(name):
    articles = ['the ', 'a ', 'an ', '?']
    for article in articles:
        if article in name:
            name = name.replace(article, '')
    return name

#Checking and removing words in the string
def checkFirstWord(string, words):
    for word in words:
        if re.findall("^" + word, string):
            return True
    return False

def solveQuestion(question):

    #Create the Parameters for Q and P
    paramsQ = {"action": "wbsearchentities", "language": "en", "format": "json", "type": "item"}
    paramsP = {"action": "wbsearchentities", "language": "en", "format": "json", "type": "property"}


    #### For questiontypes of Where/What/Who is/was/were [X's of Y]/[X of Y]
    #### X is a NN/NNS and Y is a NNP NNPS or FW
    #### Example: Where is the birth place of Bono?
    valid_question = True
    try:
        qpart = getSpacy(question, ['NNP', 'NNPS', 'FW'])
        ppart = getSpacy(question, ['NN', 'NNS'])
        # print('ppart = ', ppart, 'qpart = ', qpart)
        qNumbers = getNumbers(" ".join(qpart), paramsQ)
        pNumbers = getNumbers(" ".join(ppart), paramsP)#" ".join(ppart), paramsP)
        
    except:
        try:
            # print ("!!!")
            qpart = getSpacy(question, ['NNP', 'NNPS', 'FW', 'NN', 'NNS'])
            ppart = getSpacy(question, ['VBN', 'VB'])
            # print('ppart = ', ppart, 'qpart = ', " ".join(qpart))
            qNumbers = getNumbers(" ".join(qpart), paramsQ)
            pNumbers = getNumbers(" ".join(ppart), paramsP)
        except:
            valid_question = False

    if valid_question:
        # print("Q = ", qpart)
        # print("P = ", ppart)

        #Obtain the Q/P number
        

        if not pNumbers or not qNumbers:
            print("Could not find Q/P number")
        else:
            # print("Q = ", qNumbers[0])
            # print("P = ", pNumbers[0])

            #Create the query with the found Q and P number, and print the results
            url = "https://query.wikidata.org/sparql"
            for i in range(len(pNumbers)):
                query = "SELECT ?itemLabel WHERE { wd:" + qNumbers[0] + " wdt:" + pNumbers[i] + " ?item . SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\" . } }",
                data = requests.get(url, params={"query": query, "format": "json"}).json()
                if data["results"]["bindings"]:
                    break
            if len(pNumbers) == 0 or not data["results"]["bindings"]:
                print ("No results found")
            else:
                for item in data["results"]["bindings"]:
                    value = item["itemLabel"]["value"]
                    print("{}".format(value)) 
    else:
        print("Invalid question. Try again")


def main(argv):
    print("---Printing Example Questions---")
    printExampleQueries()
    print('---End of example---')
    print('Insert question: ')
    for line in sys.stdin:
        line = line.rstrip()
        solveQuestion(line)

if __name__ == "__main__":
    main(sys.argv)
