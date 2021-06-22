import connexion
import pandas as pd
import re

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_location_annotation import TextLocationAnnotation  # noqa: E501
from openapi_server.models.text_location_annotation_request import TextLocationAnnotationRequest  # noqa: E501
from openapi_server.models.text_location_annotation_response import TextLocationAnnotationResponse  # noqa: E501


class Data:
    def __init__(self):
        df = pd.read_csv("data/streets.csv")
        self._streets = df['Street'].str.lower().unique().tolist()

        df = pd.read_csv("data/cities.csv")
        self._cities = df['City'].str.lower().unique().tolist()

        df = pd.read_csv("data/states.csv")
        self._states = df['State'].str.lower().unique().tolist()

        df = pd.read_csv("data/countries.csv")
        self._countries = df['Name'].str.lower().unique().tolist()

        df = pd.read_csv("data/other_locations.csv")
        self._others = df['Other'].str.lower().unique().tolist()


data = Data()


def create_text_location_annotations():  # noqa: E501
    """Annotate locations in a clinical note

    Return the location annotations found in a clinical note # noqa: E501

    :param text_location_annotation_request:
    :type text_location_annotation_request: dict | bytes

    :rtype: TextLocationAnnotationResponse
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextLocationAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            note = annotation_request._note
            annotations = []

            # TODO: Add data sources
            for street in data._streets:
                matches = re.finditer(
                    r'\b({})\b'.format(street), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'street')

            for city in data._cities:
                matches = re.finditer(
                    r'\b({})\b'.format(city), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'city')

            for state in data._states:
                matches = re.finditer(
                    r'\b({})\b'.format(state), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'state')

            for country in data._countries:
                matches = re.finditer(
                    r'\b({})\b'.format(country), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'country')

            for other in data._others:
                matches = re.finditer(
                    r'\b({})\b'.format(other), note._text, re.IGNORECASE)
                add_annotations(annotations, matches, 'other')

            res = TextLocationAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status


def add_annotations(annotations, matches, location_type):
    """
    Converts matches to TextLocationAnnotation objects and adds them
    to the annotations array specified.
    """
    for match in matches:
        annotations.append(
            TextLocationAnnotation(
                start=match.start(),
                length=len(match[0]),
                text=match[0],
                location_type=location_type,
                confidence=95.5
            ))
