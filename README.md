
# Reddit Data pipeline

This pipeline involves two main stages. Initially, it retrieves data from Reddit. To achieve this, we connect to Reddit in developer mode and create an application. Once the data is obtained, we create another DAG to load it into an AWS S3 bucket.

The second part entails creating an AWS Glue job and setting up an ETL process. This process retrieves the new file from the bucket, performs some transformations, and places it into a new folder within the bucket. Subsequently, the CSV file is loaded onto Athena and Redshift for executing SQL queries and generating graphs (using Redshift).

## Architecture

```bash
    .
    ├── config
    ├── dags
    ├── data
    ├── etls
    ├── logs
    ├── pipelines
    ├── plugins
    ├── tests
    └── utils
```

## Lauch the project
You first have to create a file named config.conf into a folder config. This file will contain all your credentials like your reddit application secret and ID, your AWS secret and access key, and your airflow login and password.
After, you just have to build the project with `docker-compose up -d --build`. 
If all dags successfully done, the file will be available in your aws s3 bucked, previously created with `aws s3 mb s3://unique-name-of-your-bucket`

## Technical Stacks Used:
Airflow, AWS S3, AWS Glue, AWS Athena, RedShift, Python.
