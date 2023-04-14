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

# Script generated for node S3 accelerometer landing
S3accelerometerlanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/accelerometer/landing"],
        "recurse": True,
    },
    transformation_ctx="S3accelerometerlanding_node1",
)

# Script generated for node S3 customer trusted
S3customertrusted_node1681395669282 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://sparkling-lakes/customer/trusted"],
        "recurse": True,
    },
    transformation_ctx="S3customertrusted_node1681395669282",
)

# Script generated for node Join Customer
JoinCustomer_node2 = Join.apply(
    frame1=S3accelerometerlanding_node1,
    frame2=S3customertrusted_node1681395669282,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="JoinCustomer_node2",
)

# Script generated for node Drop Fields
DropFields_node1681396024465 = DropFields.apply(
    frame=JoinCustomer_node2,
    paths=[
        "serialNumber",
        "shareWithPublicAsOfDate",
        "birthDay",
        "registrationDate",
        "shareWithResearchAsOfDate",
        "customerName",
        "email",
        "lastUpdateDate",
        "phone",
        "shareWithFriendsAsOfDate",
    ],
    transformation_ctx="DropFields_node1681396024465",
)

# Script generated for node S3 accelerometer trusted
S3accelerometertrusted_node3 = glueContext.getSink(
    path="s3://sparkling-lakes/accelerometer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="S3accelerometertrusted_node3",
)
S3accelerometertrusted_node3.setCatalogInfo(
    catalogDatabase="sparkling_lakes", catalogTableName="accelerometer_trusted"
)
S3accelerometertrusted_node3.setFormat("json")
S3accelerometertrusted_node3.writeFrame(DropFields_node1681396024465)
job.commit()