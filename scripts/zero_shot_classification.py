from pyspark.sql import SparkSession
import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *
from pyspark.ml import Pipeline
from pyspark.ml import Pipeline, PipelineModel
import pandas as pd

# Start Spark session with Spark NLP
spark = SparkSession.builder \
    .appName("Spark NLP") \
    .master("local[*]") \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.1.4") \
    .getOrCreate()

MODEL_NAME = 'aloxatel/bert-base-mnli'

# Candidate labels for bill subjects
bill_subjects = ["health", "education", "environment", "transportation",
                "technology", "security",
                "agriculture", "employment", "budget", "taxation",
                "housing", "elections"]

#Load pre-trained ZeroShotClassification model
zero_shot_classifier = BertForZeroShotClassification.pretrained()\
    .setInputCols(["document", "token"]) \
    .setOutputCol("class") \
    .setCandidateLabels(bill_subjects)    

#Save Model
zero_shot_classifier.write().overwrite().save("./{}_spark_nlp".format(MODEL_NAME))

zero_shot_classifier_loaded = BertForZeroShotClassification.load("./{}_spark_nlp".format(MODEL_NAME))\
    .setInputCols(["document",'token'])\
        .setOutputCol("class")

#Spark Pipeline
document_assembler = DocumentAssembler() \
    .setInputCol("text") \
    .setOutputCol("document")

tokenizer = Tokenizer().setInputCols("document").setOutputCol("token")

pipeline = Pipeline(stages=[
    document_assembler,
    tokenizer,
    zero_shot_classifier_loaded
])

#Read json as a pandas df
bills_df = pd.read_json('data/filtered/NY_Assembly_bills.json')
sponsors_df = pd.read_json('data/filtered/NY_Assembly_bill_sponsors.json')

#Execute Pipeline
text = [[abstract] for abstract in bills_df["title"]]
inputDataset = spark.createDataFrame(text, ["text"])
model = pipeline.fit(inputDataset)
result = model.transform(inputDataset)
result_df = result.select("class.result").toPandas()

# Merge the results back into the original Pandas DataFrame
bills_df['subject'] = result_df["result"].str[0]

# Save as csv
bills_df.to_csv('data/processed/NY_Assembly_bills_with_subjects.csv', index=False)
sponsors_df.to_csv('data/processed/NY_Assembly_bill_sponsors.csv', index=False)


