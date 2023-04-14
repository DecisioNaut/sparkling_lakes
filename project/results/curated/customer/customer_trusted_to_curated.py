import sys

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
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

# Script generated for node S3 customer trusted
S3customertrusted_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="S3customertrusted_node1",
)

# Script generated for node S3 steptrainer trusted
S3steptrainertrusted_node1681403146748 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/steptrainer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="S3steptrainertrusted_node1681403146748",
)

# Script generated for node Rename steptrainer columns
Renamesteptrainercolumns_node1681403314509 = ApplyMapping.apply(
    frame=S3steptrainertrusted_node1681403146748,
    mappings=[
        ("serialNumber", "string", "`(right) serialNumber`", "string"),
        ("sensorReadingTime", "bigint", "sensorReadingTime", "bigint"),
        ("distanceFromObject", "bigint", "`(right) distanceFromObject`", "bigint"),
    ],
    transformation_ctx="Renamesteptrainercolumns_node1681403314509",
)

# Script generated for node Join steptrainer
S3customertrusted_node1DF = S3customertrusted_node1.toDF()
Renamesteptrainercolumns_node1681403314509DF = (
    Renamesteptrainercolumns_node1681403314509.toDF()
)
Joinsteptrainer_node2 = DynamicFrame.fromDF(
    S3customertrusted_node1DF.join(
        Renamesteptrainercolumns_node1681403314509DF,
        (
            S3customertrusted_node1DF["serialNumber"]
            == Renamesteptrainercolumns_node1681403314509DF["`(right) serialNumber`"]
        ),
        "leftsemi",
    ),
    glueContext,
    "Joinsteptrainer_node2",
)

# Script generated for node Drop Fields
DropFields_node1681403365500 = DropFields.apply(
    frame=Joinsteptrainer_node2,
    paths=[
        "`(right) serialNumber`",
        "`(right) distanceFromObject`",
        "sensorReadingTime",
    ],
    transformation_ctx="DropFields_node1681403365500",
)

# Script generated for node S3 customer curated
S3customercurated_node3 = glueContext.getSink(
    path="s3://sparkling-lakes/customer/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="S3customercurated_node3",
)
S3customercurated_node3.setCatalogInfo(
    catalogDatabase="sparkling_lakes", catalogTableName="customer_curated"
)
S3customercurated_node3.setFormat("json")
S3customercurated_node3.writeFrame(DropFields_node1681403365500)
job.commit()