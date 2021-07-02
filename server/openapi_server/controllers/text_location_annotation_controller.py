import connexion
import json
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_location_annotation import TextLocationAnnotation  # noqa: E501
from openapi_server.models.text_location_annotation_request import TextLocationAnnotationRequest  # noqa: E501
from openapi_server.models.text_location_annotation_response import TextLocationAnnotationResponse  # noqa: E501
from openapi_server import nlp_config as cf


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
            input_df = [note._text]
            spark_df = cf.spark.createDataFrame([input_df], ["text"])
            spark_df.show(truncate=70)
            embeddings = 'nlp_models/embeddings_clinical_en'
            model_name = 'nlp_models/ner_deid_large'

            ner_df = cf.get_clinical_entities(cf.spark, embeddings, spark_df, model_name)
            df = ner_df.toPandas()
            df_loc = df.loc[df['ner_label'] == 'LOCATION']

            loc_json = df_loc.reset_index().to_json(orient='records')

            loc_annotations = json.loads(loc_json)

            add_annotations(annotations, loc_annotations)
            res = TextLocationAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            print(str(error))
            res = Error("Internal error", status, str(error))
    return res, status


def add_annotations(annotations, loc_annotations):
    """
    Converts matches to TextLocationAnnotation objects and adds them
    to the annotations array specified.
    """
    for match in loc_annotations:
        annotations.append(
            TextLocationAnnotation(
                start=match['begin'],
                length=len(match['chunk']),
                text=match['chunk'],
                location_type='',
                confidence=95.5
            ))
