# Udacity's Data Engineering With AWS Nano-Degree - Project: "STEDI Human Balance Analytics"

This is a fictional project for lesson 3 of Udacity's Data Engineering with AWS nano-degree to be reviewed by Udacity.  

Although I think both, the data for this project and the rubric, are problematic (see [question 972495](https://knowledge.udacity.com/questions/972495) and [question 972946](https://knowledge.udacity.com/questions/972946) in Udacity's Knowledge Center as well as my [sense_check.ipynb](./sense_check.ipynb)) and - after more than two weeks - Udacity was not able to provide answers (let alone solutions), I herewith try my best to come up with something to finish this project.  

The overall task is to use the data provided in the [project started folder](./project/starter/) for
- [Customers](./project/starter/customer/),
- [Accelerometer data](./project/starter/accelerometer/), and
- [Step Trainer data](./project/starter/accelerometer/)  

to build a toy Datalake with
- Landing,
- Trusted, and
- Curated zones  

using AWS services
- S3,
- Glue, and
- Athena

and document the various steps by saving the Glue job scripts and Athena table definitions and also making some screenshots.

Please find the documentation here:

1. [Landing zone](./project/results/landing/)
    - [customer data](./project/results/landing/customer/)
    - [accelerometer data](./project/results/landing/accelerometer/)
    - [step trainer data](./project/results/landing/steptrainer/)
2. [Trusted zone](./project/results/trusted/)
    - [customer data](./project/results/trusted/customer/)
    - [accelerometer data](./project/results/trusted/accelerometer/)
    - [step trainer data](./project/results/trusted/steptrainer/)
3. [Curated zone](./project/results/curated/)
    - [customer data](./project/results/curated/customer/)
    - [machine learning data](./project/results/curated/machine_learning/) (combination of accelerometer and step trainer data)