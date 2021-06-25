import connexion
import re
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_id_annotation_request import TextIdAnnotationRequest  # noqa: E501
from openapi_server.models.text_id_annotation import TextIdAnnotation
from openapi_server.models.text_id_annotation_response import TextIdAnnotationResponse  # noqa: E501
import json
import nlp_config as cf


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

            input_df = [note._text]
            spark_df = cf.spark.createDataFrame([input_df], ["text"])

            embeddings = 'nlp_models/embeddings_clinical_en'
            model_name = 'nlp_models/ner_deid_large'

            ner_df = cf.get_clinical_entities(cf.spark, embeddings, spark_df, model_name)
            df = ner_df.toPandas()
            df_id = df.loc[(df['ner_label'] == 'ID') | (df['ner_label'] == 'CONTACT')]
            date_json = df_id.reset_index().to_json(orient='records')
            id_annotations = json.loads(date_json)

            add_id_annotation(annotations, id_annotations)

            res = TextIdAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            print(str(error))
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status


def add_id_annotation(annotations, id_annotations):
    """
    Converts matches to TextIdAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in id_annotations:
        annotations.append(TextIdAnnotation(
            start=match['begin'],
            length=len(match['chunk']),
            text=match['chunk'],
            id_type=id_type(match['chunk']),
            confidence=95.5
        ))


def id_type(id):
    id_types = {"ssn": (r"[\d]{3}-[\d]{2}-[\d]{4}"),
                "id_number": (r"[\d]{5,}")
                }
    found = "UNKNOWN"
    for key in id_types.keys():
        if re.search(id_types[key], id):
            found = key
            return found
        else:
            continue
    return found
