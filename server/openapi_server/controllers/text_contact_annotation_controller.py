import connexion
import re
import json
from openapi_server import nlp_config as cf
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
            input_df = [note._text]
            spark_df = cf.spark.createDataFrame([input_df], ["text"])
            spark_df.show(truncate=70)

            embeddings = 'nlp_models/embeddings_clinical_en'

            model_name = 'nlp_models/ner_deid_large'

            ner_df = cf.get_clinical_entities(cf.spark, embeddings, spark_df, model_name)

            df = ner_df.toPandas()

            df_contact = df.loc[df['ner_label'] == 'CONTACT']

            contact_json = df_contact.reset_index().to_json(orient='records')

            contact_annotations = json.loads(contact_json)
            add_contact_annotation(annotations, contact_annotations)
            res = TextContactAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            print(str(error))
            res = Error("Internal error", status, str(error))
    return res, status


def add_contact_annotation(annotations, contact_annnotations):
    """
    Converts matches to TextContactAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in contact_annnotations:
        annotations.append(TextContactAnnotation(
            start=match['begin'],
            length=len(match['chunk']),
            text=match['chunk'],
            contact_type=contact_type(match['chunk']),
            confidence=95.5
        ))


def contact_type(contact):
    contact_pattern = {"phone": (r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\
    ??\d{4}|\d{3}[-\.\s]??\d{4})"),
                       "email": (r"[\S]+@[\S]"),
                       "url": r"https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\. \
                       [^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\ \
                           .[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}"
                       }
    found = "UNKNOWN"
    for key in contact_pattern.keys():
        if re.search(contact_pattern[key], contact):
            found = key
            return found
        else:
            continue
    return found
