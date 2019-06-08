"""
Contains the `WikidataMapper` and configuration enums for getting information from Wikidata.
"""

from enum import Enum
import requests
import logging


class QueryType(Enum):
    """ The type of query used by the mapper."""

    ENTITY = "entity"
    PROPERTY = "property"


class WikidataMapper:
    """
    A mapper for property and entity strings to their Wikidata counterparts.
    """

    def __init__(self):
        self.api_url = "https://www.wikidata.org/w/api.php"

    def get_closest_map(self, phrase, query_type):
        """ Map a phrase to its Wikidata information. If the provided phrase has
        no valid URI then the result is `None`. """

        # Get the possible mappings
        maps = self.get_maps(phrase, query_type)

        # If the list is not empty
        if maps:
            # Return the closest mapping
            return maps[0]

        # If there is no closest mapping
        return None

    def get_maps(self, phrase, query_type):
        """ Map a phrase to possible Wikidata entries. """

        # Prepare the general parameters to be sent in the Wikidata query
        params = {
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": phrase,
        }

        # Add additional parameters based on the query type.
        if query_type == QueryType.ENTITY:
            pass
        elif query_type == QueryType.PROPERTY:
            params["type"] = query_type.value
        else:
            raise ValueError(
                "query_type must be a valid QueryType: {}".format(list(QueryType))
            )

        # Request data from the API.
        json = requests.get(self.api_url, params=params).json()

        # Prepare to extract the mappings.
        maps = []

        try:
            # Attempt to extract the "search"
            results = json["search"]

            for result in results:
                # Extract the label
                label = result["label"]
                # Extract the URI
                uri = result["id"]
                # Extract the description. Some results do not have a
                # description. In that case the description is set to None.
                try:
                    description = result["description"]
                except KeyError:
                    description = None
                # Add the extracted information to the maps.
                maps.append({"label": label, "uri": uri, "description": description})
        except KeyError as exception:
            print(
                "{} is providing malformed JSON (perhaps due to a rate limit?)".format(
                    self.api_url
                )
            )
            print(json)
            raise exception

        logging.debug("%s maps to %s", phrase, maps)
        return maps
