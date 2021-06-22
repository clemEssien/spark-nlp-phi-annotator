import connexion
import pandas as pd
import re

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_person_name_annotation_request import TextPersonNameAnnotationRequest  # noqa: E501
from openapi_server.models.text_person_name_annotation import TextPersonNameAnnotation  # noqa: E501
from openapi_server.models.text_person_name_annotation_response import TextPersonNameAnnotationResponse  # noqa: E501


class Data:
    def __init__(self):
        # https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt.html
        firstnames_df = pd.read_csv("data/first_names.csv")
        # Top 1000 last names from census.gov (18-10-2020)
        # https://www.census.gov/topics/population/genealogy/data/2000_surnames.html
        lastnames_df = pd.read_csv("data/last_names.csv")

        # Append all names
        names = firstnames_df['firstname'].append(lastnames_df['lastname'])
        self._names = names.str.lower().unique().tolist()


data = Data()


def create_text_person_name_annotations():  # noqa: E501
    """Annotate person names in a clinical note

    Return the person name annotations found in a clinical note # noqa: E501

    :rtype: TextPersonNameAnnotationResponse
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextPersonNameAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            note = annotation_request._note  # noqa: E501
            annotations = []

            for name in data._names:
                if name in note._text.lower():
                    matches = re.finditer(
                        r'\b({})\b'.format(name), note._text, re.IGNORECASE)
                    for match in matches:
                        annotations.append(TextPersonNameAnnotation(
                            start=match.start(),
                            length=len(match[0]),
                            text=match[0],
                            confidence=95.5
                        ))
            res = TextPersonNameAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status
