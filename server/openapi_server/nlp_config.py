import os
from sparknlp.annotator import NerConverter, NerDLModel, SentenceDetector, Tokenizer, WordEmbeddingsModel
from sparknlp.base import DocumentAssembler
import sparknlp_jsl
from pyspark.ml import Pipeline
import pyspark.sql.functions as F
from pyspark.sql.functions import monotonically_increasing_id


class Spark:
    def __init__(self):
        # create nlp spark session
        params = {"spark.driver.memory": "16G",
                  "spark.kryoserializer.buffer.max": "2000M",
                  "spark.driver.maxResultSize": "2000M"}
        self.spark = sparknlp_jsl.start(os.environ['JSL_SECRET'], params=params)

spark = Spark().spark


def get_base_pipeline(embeddings):

    documentAssembler = DocumentAssembler()\
      .setInputCol("text")\
      .setOutputCol("document")

    # Sentence Detector annotator, processes various sentences per line
    sentenceDetector = SentenceDetector().setInputCols(["document"]).setOutputCol("sentence")

    # Tokenizer splits words in a relevant format for NLP
    tokenizer = Tokenizer().setInputCols(["sentence"]).setOutputCol("token")

    # Clinical word embeddings trained on PubMED dataset
    word_embeddings = WordEmbeddingsModel.load(embeddings)\
        .setInputCols(["sentence", "token"])\
        .setOutputCol("embeddings")

    base_pipeline = Pipeline(stages=[
                    documentAssembler,
                    sentenceDetector,
                    tokenizer,
                    word_embeddings
                  ])

    return base_pipeline


def get_clinical_entities(spark, embeddings, spark_df, model_name):

    # NER model trained on i2b2 (sampled from MIMIC) dataset
    loaded_ner_model = NerDLModel.load(model_name) \
      .setInputCols(["sentence", "token", "embeddings"]) \
      .setOutputCol("ner")

    ner_converter = NerConverter() \
        .setInputCols(["sentence", "token", "ner"]) \
        .setOutputCol("ner_chunk")

    base_pipeline = get_base_pipeline(embeddings)

    nlpPipeline = Pipeline(stages=[
      base_pipeline,
      loaded_ner_model,
      ner_converter])

    empty_data = spark.createDataFrame([[""]]).toDF("text")

    model = nlpPipeline.fit(empty_data)

    result = model.transform(spark_df)
    result = result.withColumn("id", monotonically_increasing_id())

    result_df = result.select('id', F.explode(F.arrays_zip('ner_chunk.result', 'ner_chunk.begin',
                              'ner_chunk.end', 'ner_chunk.metadata')).alias("cols")) \
                      .select('id', F.expr("cols['3']['sentence']").alias("sentence_id"),
                              F.expr("cols['0']").alias("chunk"),
                              F.expr("cols['1']").alias("begin"),
                              F.expr("cols['2']").alias("end"),
                              F.expr("cols['3']['entity']").alias("ner_label"))\
                      .filter("ner_label!='O'")
    return result_df
