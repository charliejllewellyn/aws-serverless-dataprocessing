# Overview
This lab demonstrates how to build a serverless data processing pipeline to enrich data, catalog it and run add hock queries and reporting.

The lab also introduces AWS Codepipeline enabling blue/green deployments of the serverless application.

# Prerequisites

# Implementation
The follow steps lead you through the process of deploying and testing the application.
## Creating a pipeline to automatically deploy our application
The first step in our development cycle is to implement a codepipeline to automatically test, build and deploy our application.

Doing this via the AWS can be a time consuming task so we'll first deploy a CloudFormation script which will setup the majority of the pipeline and associated IAM roles and CodeBuild steps.

To do this click on the following link which will open the AWS CloudFormation console and load hte template ready for deployment.

| AWS Region | Short name | |
| -- | -- | -- |
| EU West (London) | eu-west-2 | <a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=serverlessdataprocessing&templateURL=https://s3-eu-west-1.amazonaws.com/aws-shared-demo-cf-templates/codepipeline/codepipeline.yaml" target="_blank"><img src="images/cloudformation-launch-stack.png"></a> |

pip install nose2 boto3 && nose2 -v
## Create a step function to perform data processing
## Create a glue catalog
## Query QuickSight
SELECT 
labels2.name, labels2.confidence
FROM 
cheltworkshop.rekognitionimagedetectlabels  CROSS JOIN UNNEST(labels) as t(labels2)
## Use Athena to query data
SELECT 
labels2.name, labels2.confidence
FROM 
cheltworkshop.rekognitionimagedetectlabels  CROSS JOIN UNNEST(labels) as t(labels2)
## Demonstrate blue/green
