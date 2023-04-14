# Sparkling Lakes
Part 3 of Udacity's Data Engineering With AWS Nano-Degree

In this lesson of the course, it was all about data lakes and lakehouses and how to handle them using [Apache Spark](https://spark.apache.org/), and later going serverless using [AWS Glue](https://aws.amazon.com/glue/), pulling data from [AWS S3 buckets](https://aws.amazon.com/s3/) and querying the data using [AWS Athena](https://aws.amazon.com/athena/).  

In this project, the task is to help a fictional company named _STEDI_ with their Data Engineering tasks.  

STEDI developed a _Step Trainer_, an IoT device helping users to train their balance. The Step Trainer itself is a motion sensor that collects data to train a machine learning model to detect steps. In addition there's a companion mobile app that collects customer data and interacts with the device sensors. For more information, also visit the following [YouTube video on STEDI](https://www.youtube.com/watch?v=__dI0Ocjd1Q&t=20s).

The STEDI team asked for extracting the data produced by the STEDI Step Trainer and the mobile app (both stored in S3 buckets), and curate them into a data lakehouse solution on AWS so that the Data Science team can train their machine learning model. The curated data should respect customers privacy and should only be used for research when the customer explicitly agreed to it / opted in.

For the overall process, we'll use the following stack and AWS services:
- Python and Apache Spark
- AWS S3 buckets
- AWS Glue
- AWS Athena

As typical for a data lakehouse solution, we'll have three zones:
- __Landing Zone__: The raw data from the mobile app and the Step Trainer
- __Trusted Zone__: The data from the Landing Zone, but sanitized and only containing data from customers who agreed to share their data for research purposes
- __Curated Zone__: The data from the Trusted Zone, but sanitized and only containing data from customers who have accelerometer data and have agreed to share their data for research

AWS Glue and AWS Athena are serverless services, which, at the startup phase of the company, would be a good choice to save money. However, as the company grows, it might be a good idea to switch to a more traditional data lakehouse solution.

## Project Structure / Documentation

To document my work, as required by Udacity, this repo includes:  
- A Python script [`customer_trusted.py`](./project/results/customer_trusted.py) using Spark (creating a Glue Table `customer_trusted`) that sanitizes the customer data from the website in the Landing Zone and only stores the customer records who agreed to share their data for research purposes in the Trusted Zone.
- A Python script [`accelerometer_trusted.py`](./project/results/accelerometer_trusted.py) using Spark (creating a Glue Table `accelerometer_trusted`) that sanitizes the accelerometer data from the mobile app in the Landing Zone and only stores accelerometer readings from customers who agreed to share their data for research purposes in the Trusted Zone.
- A Python script [`customer_curated.py`]() that sanitizes the customer data from the Trusted Zone and only stores the customers who have accelerometer data and have agreed to share their data for research in the Curated Zone in a Glue Table called `customer_curated`.
- A Python script [`step_trainer_trusted.py`]() that read the Step Trainer IoT data stream from the Landing Zone and populates a Glue Table called step_trainer_trusted containing the Step Trainer records for customers who have accelerometer data and have agreed to share their data for research (linked to the customer_curated Glue Table able) in a Glue Table called `step_trainer_trusted` in the Trusted Zone.
- A Python script [`step_trainer_curated.py`]() that has each of the Step Trainer readings, and the associated accelerometer reading data for the same timestamp, but only for customers who have accelerometer data and have agreed to share their data, and populates a Glue Table called `machine_learning_curated` in the Curated Zone.
- SQL queries [`customer_landing.sql`](./project/results/customer_landing.sql) and [`accelerometer_landing.sql`](./project/results/accelerometer_landing.sql) to query the respective Glue Tables in the Landing Zone along with sceenshots [`customer_landing.png`](./project/results/customer_landing.png) and [`accelermeter_landing.png`](./project/results/accelerometer_landing.png). In the `customer_landing.png` we can also see that there are entries for customers who have not agreed to share their data for research (the `sharewithresearchasofdate` field is empty).
- A screenshot of my Athena query of the `customer_trusted` Glue Table [`customer_trusted.png`]().

## Fulfilling the Project Specifications from Udacity
I must say that Udacity's is getting quite sloppy in designing the courses. Whilst the project states the task above, the project rubric is a bit different and sometimes confusing. The rubric states that the following should be done:

__Landing Zone__  

| Criteria | Meets Specifications | Link to Documentation |
| --- | --- | --- |
| Use Glue Studio to ingest data from an S3 bucket | customer_landing_to_trusted.py and accelerometer_landing_to_trusted_zone.py Glue jobs have a node that connects to S3 bucket for customer and accelerometer landing zones. | Weirdly, Udacity names these scripts as "to_trusted" although this is meant to be in the landing zone! Here are to scripts for ingesting the data to landing tables, but with Udacity's weird naming: [`customer_landing_to_trusted.py`](./project/results/for_rubics_mess/customer_landing_to_trusted.py) and [`accelerometer_landing_to_trusted`](./project/results/for_rubics_mess/accelerometer_landing_to_trusted.py)  |
| Manually create a Glue Table using Glue Console from JSON data | SQL DDL scripts customerlanding.sql and accelerometer_landing.sql include all of the JSON fields in the data input files, and are appropriately typed (not everything is a string) | Did you recognize that Udacity spells the customer script a bit different here? Ok, there you go: [`customerlanding.sql`](./project/results/customercustomlanding.sql) and [`accelerometer_landing.sql`](./project/results/accelerometer_landing.sql) |
| Use Athena to query the Landing Zone. | Screenshot shows a select statement from Athena showing the customer landing data and accelerometer landing data, where the customer landing data has multiple rows where shareWithResearchAsOfDate is blank. | [Query result of customer_landing that do not opt in](./project/results/customer_landing_with_not_opting_in.png) |

__Trusted Zone__  

| Criteria | Meets Specifications | Link to Documentation |
| --- | --- | --- |
| Configure Glue Studio to dynamically update a Glue Table schema from JSON data | Glue Job Python code shows that the option to dynamically infer and update schema is enabled. | Whatever this means. I think it is enabled by all of my scripts that directly pull from S3. |
| Use Athena to query Trusted Glue Tables | A screenshot that shows a select * statement from Athena showing the customer landing data, where the resulting customer trusted data has no rows where shareWithResearchAsOfDate is blank. | [Query result of customer_trusted that do not opt in](./project/results/customer_trusted_with_not_opting_in.png) |
| Join Privacy tables with Glue Jobs | Glue jobs have inner joins that join up with the customer_landing table on the serialnumber field. (customer_landing_to_trusted.py and accelerometer_landing_to_trusted_zone.py) | Here the craziness overwhelms me: the accelerometer data doesn't have a `serialnumber` field. I can only guess that they mean the `email` and `user` field. Ok, then here you go: [`customer_landing_to_trusted.py`](./project/results/customer_landing_to_trusted.py) and [`accelerometer_landing_to_trusted`](./project/results/accelerometer_landing_to_trusted.py) |
| Filter protected PII with Spark in Glue Jobs | Glue jobs drop data that doesn’t have data in the sharedWithResearchAsOfDate column (customer_landing_to_trusted.py and accelerometer_landing_to_trusted_zone.py) | This is then included in the above... |

__Curated Zone__  

| Criteria | Meets Specifications | Link to Documentation |
| --- | --- | --- |
| Write a Glue Job to join trusted data | Glue jobs do inner joins with the customer_trusted table. (Customer_trusted_to_curated.py and trainer_trusted_to_curated.py) | ... |
| Write a Glue Job to create curated data | The curated data from the Glue tables is sanitized and only contains only customer data from customer records that agreed to share data, and is joined with the correct accelerometer data. | ... |


Please note, that all the AWS resources targeted by the scripts were created only for the purpose of the Udacity course and will be deleted after the course is finished.

## Data and more on the requirements

The data is stored in S3 buckets / Landing Zone and has the following structure:

Customer data is stored in JSON format on [s3://sparkling-lakes/customers/landing/](s3://sparkling-lakes/customers/landing/):
```
{
    "customerName":"######### ######",
    "email":"#########.######@####.###",
    "phone":"##########",
    "birthDay":"####-##-##",
    "serialNumber":"3fe69104-657e-45a1-bd6e-fece3e42de85",
    "registrationDate":1655296158613,
    "lastUpdateDate":1655296193801,
    "shareWithResearchAsOfDate":1655296193801,
    "shareWithPublicAsOfDate":1655296193801,
    "shareWithFriendsAsOfDate":1655296193801
}
```

If customers have opted in to having their data used for research, the `shareWithResearchAsOfDate` field is not zero. Only those customers should be included in the `customer_trusted` Glue Table.

The Step Trainer data is stored in JSON format on [s3://sparkling-lakes/step-trainer/landing/](s3://sparkling-lakes/step-trainer/landing/):
```
{
    "sensorReadingTime":1655296621164,
    "serialNumber":"ece6edf8-a14c-4489-a41c-98fe1b72b059",
    "distanceFromObject":209
}
```  

The accelerometer data is stored in JSON format on [s3://sparkling-lakes/mobile-app/landing/](s3://sparkling-lakes/mobile-app/landing/):
```
{
    "user":"#####.#####@####.###",
    "timeStamp":1655562565701,
    "x":0.0,
    "y":-1.0,
    "z":0.0
}
```  

The Data Scientists have discovered a data quality issue with the Customer Data. The serial number should be a unique identifier for the STEDI Step Trainer they purchased. However, there was a defect in the fulfillment website, and it used the same 30 serial numbers over and over again for millions of customers! Most customers have not received their Step Trainers yet, but those who have, are submitting Step Trainer data over the IoT network (Landing Zone). The data from the Step Trainer Records has the correct serial numbers.

The Data Science team would like to Data Engineering to write a Glue job that does the following:

- Sanitize the Customer data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who have accelerometer data and have agreed to share their data for research called customers_curated.

Finally, you need to create two Glue Studio jobs that do the following tasks:

- Read the Step Trainer IoT data stream (S3) and populate a Trusted Zone Glue Table called step_trainer_trusted that contains the Step Trainer Records data for customers who have accelerometer data and have agreed to share their data for research (customers_curated).
- Create an aggregated table that has each of the Step Trainer Readings, and the associated accelerometer reading data for the same timestamp, but only for customers who have agreed to share their data, and make a glue table called machine_learning_curated.

Please note that this repo contains [parts provided by Udacity](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises), namely the lesson-x folders and the project folder. These parts underly the [license](./LICENSE.md) from Udacity, which is added to this repo.

P.S.: For the exercises, I've installed Apache Spark on my local machine (MacOS) roughly following [this guide](https://towardsdatascience.com/how-to-get-started-with-pyspark-1adc142456ec). I must say that it was a painful experience. E.g. newest python version(s) seem not to work well with newest PySpark, so I went back to python3.8, and there were also some low level things in config-files I needed do to to get rid of warning messages (of course, you can survive without doing these things, but it tends to make me nervous).