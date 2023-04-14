import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 accelerometer trusted
S3accelerometertrusted_node1681405775392 = (
    glueContext.create_dynamic_frame.from_options(
        format_options={"multiline": False},
        connection_type="s3",
        format="json",
        connection_options={
            "paths": ["s3://sparkling-lakes/accelerometer/trusted/"],
            "recurse": True,
        },
        transformation_ctx="S3accelerometertrusted_node1681405775392",
    )
)

# Script generated for node S3 steptrainer trusted
S3steptrainertrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/steptrainer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="S3steptrainertrusted_node1",
)

# Script generated for node Join steptrainer accelerometer
Joinsteptraineraccelerometer_node1681407159147 = Join.apply(
    frame1=S3steptrainertrusted_node1,
    frame2=S3accelerometertrusted_node1681405775392,
    keys1=["sensorReadingTime"],
    keys2=["timeStamp"],
    transformation_ctx="Joinsteptraineraccelerometer_node1681407159147",
)

# Script generated for node Drop Fields
DropFields_node1681407243545 = DropFields.apply(
    frame=Joinsteptraineraccelerometer_node1681407159147,
    paths=["sensorReadingTime"],
    transformation_ctx="DropFields_node1681407243545",
)

# Script generated for node Amazon S3
AmazonS3_node1681407328570 = glueContext.getSink(
    path="s3://sparkling-lakes/machinelearning/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1681407328570",
)
AmazonS3_node1681407328570.setCatalogInfo(
    catalogDatabase="sparkling_lakes", catalogTableName="machine_learning_curated"
)
AmazonS3_node1681407328570.setFormat("json")
AmazonS3_node1681407328570.writeFrame(DropFields_node1681407243545)
job.commit()