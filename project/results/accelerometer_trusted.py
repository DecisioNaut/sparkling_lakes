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

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/accelerometer/landing"],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1680100718539 = glueContext.create_dynamic_frame.from_catalog(
    database="sparkling_lakes",
    table_name="customer_trusted",
    transformation_ctx="AWSGlueDataCatalog_node1680100718539",
)

# Script generated for node Join
Join_node1680100708902 = Join.apply(
    frame1=S3bucket_node1,
    frame2=AWSGlueDataCatalog_node1680100718539,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="Join_node1680100708902",
)

# Script generated for node Drop Fields
DropFields_node1680100781388 = DropFields.apply(
    frame=Join_node1680100708902,
    paths=[
        "customername",
        "email",
        "phone",
        "birthday",
        "serialnumber",
        "registrationdate",
        "lastupdatedate",
        "sharewithresearchasofdate",
        "sharewithpublicasofdate",
        "sharewithfriendsasofdate",
    ],
    transformation_ctx="DropFields_node1680100781388",
)

# Script generated for node Amazon S3
AmazonS3_node1680103191938 = glueContext.getSink(
    path="s3://sparkling-lakes/accelerometer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1680103191938",
)
AmazonS3_node1680103191938.setCatalogInfo(
    catalogDatabase="sparkling_lakes", catalogTableName="accelerometer_trusted"
)
AmazonS3_node1680103191938.setFormat("json")
AmazonS3_node1680103191938.writeFrame(DropFields_node1680100781388)
job.commit()