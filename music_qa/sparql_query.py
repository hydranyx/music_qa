import requests
import sys
import urllib.parse

SPARQL_URL = "https://query.wikidata.org/sparql"


def run_query(query):
    """ Run the provided query string on the Wikidata SPARQL Endpoint. """
    # Prepare the url
    full_url = SPARQL_URL + "?query=" + urllib.parse.quote_plus(query)
    # Prepare the parameters asking for JSON
    params = {"language": "en", "format": "json"}
    # Make the request
    result = requests.get(full_url, params)

    # If the request was unsuccesful
    if result.status_code != 200:
        raise RuntimeError("Error communicating with SPARQL end point")

    # If there are results
    result = result.json()
    if result["results"]["bindings"]:
        variables = result["head"]["vars"]
        # Extract the data to be printed
        data = result["results"]["bindings"]
        answer = []
        for result in data:
            for var in variables:
                answer.append(result[var]["value"])
        return answer

    return None
