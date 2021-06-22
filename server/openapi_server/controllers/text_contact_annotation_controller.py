import connexion
import re
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_contact_annotation_request import TextContactAnnotationRequest  # noqa: E501
from openapi_server.models.text_contact_annotation import TextContactAnnotation
from openapi_server.models.text_contact_annotation_response import TextContactAnnotationResponse  # noqa: E501


def create_text_contact_annotations(text_contact_annotation_request=None):  # noqa: E501
    """Annotate contacts in a clinical note
    Return the Contact annotations found in a clinical note # noqa: E501
    :param text_contact_annotation_request:
    :type text_contact_annotation_request: dict | bytes
    :rtype: TextContactAnnotationResponse
    """
    if connexion.request.is_json:
        try:
            annotation_request = TextContactAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            note = annotation_request._note
            print(note)
            annotations = []
            matches = re.finditer(r"\([\d]{3}\)\s[\d]{3}-[\d]{4}", note._text)
            add_contact_annotation(annotations, matches, "phone")

            matches = re.finditer(r"[\d]{3}-[\d]{3}-[\d]{4}", note._text)
            add_contact_annotation(annotations, matches, "phone")

            matches = re.finditer(r"[\S]+@[\S]+", note._text)
            add_contact_annotation(annotations, matches, "email")

            matches = re.finditer(r"https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}", note._text)  # noqa: E501
            add_contact_annotation(annotations, matches, "url")
            res = TextContactAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status


def add_contact_annotation(annotations, matches, contact_type):
    """
    Converts matches to TextContactAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in matches:
        annotations.append(TextContactAnnotation(
            start=match.start(),
            length=len(match[0]),
            text=match[0],
            contact_type=contact_type,
            confidence=95.5
        ))
