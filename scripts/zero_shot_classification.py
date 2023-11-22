from pyspark.sql import SparkSession
import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *
from pyspark.ml import Pipeline
from pyspark.ml import Pipeline, PipelineModel

# Start Spark session with Spark NLP
spark = SparkSession.builder \
    .appName("Spark NLP") \
    .master("local[*]") \
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:5.1.4") \
    .getOrCreate()

MODEL_NAME = 'aloxatel/bert-base-mnli'

# Candidate labels for bill subjects
bill_subjects = ["Healthcare", "Education", "Environment", "Economy", "Transportation", 
                "Technology", "Welfare", "Justice", "Public Safety", 
                "Agriculture", "Energy", "Labor and Employment", "Budget", "Taxes"
                "Housing", "Foreign Policy"]

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


    
# Load JSON data
df = spark.read.json('data/filtered/NY_Assembly_bills.json')


zero_shot_classifier_loaded = BertForZeroShotClassification.load("./{}_spark_nlp".format(MODEL_NAME))\
    .setInputCols(["document",'token'])\
        .setOutputCol("class")

document_assembler = DocumentAssembler() \
    .setInputCol("text") \
    .setOutputCol("document")

tokenizer = Tokenizer().setInputCols("document").setOutputCol("token")

pipeline = Pipeline(stages=[
    document_assembler,
    tokenizer,
    zero_shot_classifier_loaded
])

# create a DataFrame in PySpark
inputDataset = spark.createDataFrame(text, ["text"])
model = pipeline.fit(inputDataset)
model.transform(inputDataset).select("class.result").show()