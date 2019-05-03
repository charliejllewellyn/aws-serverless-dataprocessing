# Overview
This lab demonstrates how to build a serverless data processing pipeline to enrich data, catalog it and run add hock queries and reporting.

The lab also introduces AWS Codepipeline enabling blue/green deployments of the serverless application.

# Prerequisites

# Implementation
The follow steps lead you through the process of deploying and testing the application.
## Creating a pipeline to automatically deploy our application
The first step in our development cycle is to implement a codepipeline to automatically test, build and deploy our application.

Doing this via the AWS console can be a time consuming task so we'll first deploy a CloudFormation script which will setup the majority of the pipeline and associated IAM roles and CodeBuild steps.

To do this click on the following link which will open the AWS CloudFormation console and load hte template ready for deployment.

| AWS Region | Short name | |
| -- | -- | -- |
| EU West (London) | eu-west-2 | <a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=serverlessdataprocessing&templateURL=https://s3-eu-west-1.amazonaws.com/aws-shared-demo-cf-templates/codepipeline/codepipeline.yaml" target="_blank"><img src="images/cloudformation-launch-stack.png"></a> |

1. On the page that opens click **next**
1. Enter a project name e.g. *serverlessdataprocessing* and click **next**
1. Click **next**
1. Place a check in **I acknowledge that AWS CloudFormation might create IAM resources with custom names.**
    <p align="left">
      <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/cf_iam_perms.png">
    </p>
1. Click **Create Stack**

This will take approximatly 5 minutes to deploy the stack and should result in CREATE_COMPLETE.

<p align="left">
  <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/cf_create_complete.png">
</p>

Once our pipeline is deployed we're going to add an additional stage. This stage will run a CodeBuild job to first execute our unitests before continuing to prepare and deploy the application.

### Add a CodePiple stage for unitesting

1. In the top left of the AWS console select **services**
1. In the search box enter *CodePipeline* and select the service
<p align="left">
  <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/svc_codepipline.png">
</p>

pip install nose2 boto3 && nose2 -v
## Create a step function to perform data processing
Start generating traffic with lambda function
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
