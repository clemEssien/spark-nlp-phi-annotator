import connexion
import re
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_id_annotation_request import TextIdAnnotationRequest  # noqa: E501
from openapi_server.models.text_id_annotation import TextIdAnnotation
from openapi_server.models.text_id_annotation_response import TextIdAnnotationResponse  # noqa: E501


def create_text_id_annotations(text_id_annotation_request=None):  # noqa: E501
    """Annotate IDs in a clinical note

    Return the ID annotations found in a clinical note # noqa: E501

    :param text_id_annotation_request:
    :type text_id_annotation_request: dict | bytes

    :rtype: TextIdAnnotationResponse
    """
    if connexion.request.is_json:
        try:
            annotation_request = TextIdAnnotationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            note = annotation_request._note
            annotations = []
            matches = re.finditer(r"[\d]{3}-[\d]{2}-[\d]{4}", note._text)
            add_id_annotation(annotations, matches, "ssn")

            matches = re.finditer(r"[\d]{5,}", note._text)
            add_id_annotation(annotations, matches, "id_number")
            res = TextIdAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status


def add_id_annotation(annotations, matches, id_type):
    """
    Converts matches to TextIdAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in matches:
        annotations.append(TextIdAnnotation(
            start=match.start(),
            length=len(match[0]),
            text=match[0],
            id_type=id_type,
            confidence=95.5
        ))
