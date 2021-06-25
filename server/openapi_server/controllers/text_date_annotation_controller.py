import connexion
import re
import json

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_date_annotation_request import \
    TextDateAnnotationRequest  # noqa: E501
from openapi_server.models.text_date_annotation import TextDateAnnotation
from openapi_server.models.text_date_annotation_response import \
    TextDateAnnotationResponse  # noqa: E501
import nlp_config as cf


def create_text_date_annotations():  # noqa: E501
    """Annotate dates in a clinical note

    Return the date annotations found in a clinical note # noqa: E501

    :rtype: TextDateAnnotations
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextDateAnnotationRequest.from_dict(
                connexion.request.get_json())  # noqa: E501
            note = annotation_request._note

            annotations = []
            print(note._text)
            input_df = [note._text]
            spark_df = cf.spark.createDataFrame([input_df], ["text"])
            spark_df.show(truncate=70)

            embeddings = 'nlp_models/embeddings_clinical_en'
            model_name = 'nlp_models/ner_deid_large'

            ner_df = cf.get_clinical_entities(cf.spark, embeddings, spark_df, model_name)
            df = ner_df.toPandas()

            df_date = df.loc[df['ner_label'] == 'DATE']
            date_json = df_date.reset_index().to_json(orient='records')

            date_annotations = json.loads(date_json)
            add_date_annotation(annotations, date_annotations)
            res = TextDateAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            print(str(error))
            res = Error("Internal error", status, str(error))
    return res, status


def get_date_format(date_str):
    date_pattern = {"MM/DD/YYYY": "([1-9]|0[1-9]|1[0-2])(/)\
                    ([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(/)(19[0-9][0-9]|20[0-9][0-9])",
                    "DD.MM.YYYY": "([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\\.)([1-9]|0[1-9]\
                    |1[0-2])(\\.)(19[0-9][0-9]|20[0-9][0-9])",
                    "YYYY": "([1-9][1-9][0-9][0-9]|2[0-9][0-9][0-9])",
                    "MMMM": "(January|February|March|April|May|June|July|August|September|October|November|December)"
                    }
    found = 'UNKNOWN'
    for key in date_pattern.keys():
        if re.search(date_pattern[key], date_str):
            found = key
            return found
        else:
            continue
    return found


def add_date_annotation(annotations, date_annotations):
    """
    Converts matches to TextDateAnnotation objects and adds them to the
    annotations array specified.
    """
    for match in date_annotations:
        annotations.append(TextDateAnnotation(
            start=match['begin'],
            text=match['chunk'],
            length=len(match['chunk']),
            date_format=get_date_format(match['chunk']),
            confidence=95.5
        ))
