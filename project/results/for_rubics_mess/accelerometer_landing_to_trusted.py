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
    format_options={"multiline": True},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/accelerometer/landing"],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1680091957474 = glueContext.write_dynamic_frame.from_catalog(
    frame=S3bucket_node1,
    database="sparkling_lakes",
    table_name="accelerometer_landing",
    additional_options={
        "enableUpdateCatalog": True,
        "updateBehavior": "UPDATE_IN_DATABASE",
    },
    transformation_ctx="AWSGlueDataCatalog_node1680091957474",
)

job.commit()