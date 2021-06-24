import connexion
import pandas as pd
import re

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_person_name_annotation_request import TextPersonNameAnnotationRequest  # noqa: E501
from openapi_server.models.text_person_name_annotation import TextPersonNameAnnotation  # noqa: E501
from openapi_server.models.text_person_name_annotation_response import TextPersonNameAnnotationResponse  # noqa: E501

import json
import nlp_config as cf
class Spark:
    def __init__(self):
        # https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt.html
        firstnames_df = pd.read_csv("data/first_names.csv")
        # Top 1000 last names from census.gov (18-10-2020)
        # https://www.census.gov/topics/population/genealogy/data/2000_surnames.html
        lastnames_df = pd.read_csv("data/last_names.csv")

        # Append all names
        session = cf.init_spark()


spark = Spark()


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

            input_df = [note._text]
            spark_df = spark._session.createDataFrame([input_df],["text"])
                            

            spark_df.show(truncate=70)

            embeddings = 'nlp_models/embeddings_clinical_en'

            model_name = 'nlp_models/ner_deid_large'


            ner_df = cf.get_clinical_entities (spark._session, embeddings, spark_df,model_name)

            df = ner_df.toPandas()

            df_name = df.loc[df['ner_label'] == 'name']

            name_json = df_name.reset_index().to_json(orient='records')

            name_annotations = json.loads(name_json)

            for match in name_annotations:
                annotations.append(TextPersonNameAnnotation(
                            start=match['begin'],
                            length=len(match['chunk']),
                            text=match['chunk'],
                            confidence=95.5
                        ))
            res = TextPersonNameAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    return res, status
