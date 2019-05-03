# Overview
This lab demonstrates how to build a serverless data processing pipeline to enrich data, catalog it and run ad-hoc queries and reporting.

The lab also introduces AWS Codepipeline enabling blue/green deployments of the serverless application.

# Prerequisites

Install Git, generate a keypair and add add the public key to your security credentials in AWS. The can be done by following the guide here:

https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html

**Note:** You can skip **Step 4**

# Implementation
The follow steps lead you through the process of deploying and testing the application.
## Creating a pipeline to automatically deploy our application
The first step in our development cycle is to implement a codepipeline to automatically test, build and deploy our application.

Doing this via the AWS console can be a time consuming task so we'll first deploy a CloudFormation script which will setup the majority of the pipeline and associated IAM roles and CodeBuild steps.

To do this click on the following link which will open the AWS CloudFormation console and load hte template ready for deployment.

| AWS Region | Short name | |
| -- | -- | -- |
| EU West (London) | eu-west-2 | <a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=serverlessdataprocessing&templateURL=https://s3-eu-west-1.amazonaws.com/aws-shared-demo-cf-templates/codepipeline/code-pipeline.yaml" target="_blank"><img src="images/cloudformation-launch-stack.png"></a> |

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
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/svc_codepipline.png">
    </p>
1. Click into the pipeline you have created e.g. *serverlessdataprocessing-Codepipeline-Demo*
    **Note:** It will show failed because it doesn't yet have any code to deploy
1. In the top left click edit
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/codepipeline_edit.png">
    </p>
1. Underneath the first phase *Source* click **Add Stage**.
1. Enter *Testing* for the **Stage Name** and click **Add Stage**
1. In the new stage click **Add action group**
1. Enter *unitests* for the **Action name**
1. Select **AWS CodeBuild** under the **Test** section for the **Action provider**
1. Leave the **Region** as **EU (Ireland)**
1. Select **MyApp** for the **Input artifacts**
1. Select **Create Project** for the **Project Name**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/codebuild_stage.png">
    </p>
1. In page that opens enter *unitests* as the **Project Name**
1. Unless specified below leave all other fields as their default
1. In the **Environment** section select **Ubuntu** as the **Operating system**
1. Select **Python** for the **Runtime(s)**
1. Select **aws/codebuild/python:3.7.1** for the **Image version**
1. Place a check in **Existing Service Role**
1. Select the role **serverlessdataprocessing-Codepipeline-Codebuild-Role**
1. Under the **Buildspec** section check **Insert build commands**
1. In the **Build commands** box enter the following
    ```pip install nose2 boto3 && nose2 -v```
1. Click **Continue to CodePipeline**
1. Once you are returned to the previous window click **Save**
1. On the next page click **Save**
1. Finally click **Save** on the popup

### Deploy the application

1. Within the CodePipeline console expand **source** in the left maneu and select **repositories**
1. Select **SSH** on the right hand side next to the **serverelessdataprocessing** repository
1. On your local computer checkout the code from the repository address you just copied e.g.
    ```git clone ssh://git-codecommit.eu-west-1.amazonaws.com/v1/repos/serverlessdataprocessing```
1. On your local computer clone the example application from https://github.com/charliejllewellyn/aws-service-demos, e.g.
   ```git clone https://github.com/charliejllewellyn/aws-service-demos```
1. On your local computer copy the code from aws-service-demos/codepipeline/exampleDeployment/* into the CodeCommit repostory you checked out in step 3, e.g.
    ```cp -R aws-service-demos/codepipeline/exampleDeployment/* serverlessdataprocessing/```
1. On your local computer checkin the changes and push the application e.g.
    ```cd serverlessdataprocessing/ && git add * && git commit -m 'inital code deployment' && git push```
1. Head back to the CodePipeline console and expand **Pipeline** on the left and select **Pipelines**
1. Click into your pipeline e.g. *serverlessdataprocessing-Codepipeline-Demo* and you can follow the progress

## Create a step function to perform data processing

### Generate application traffic
To simulate a real world application we'll start generating some real data to process. To help with this we've written a Lambda function that uses an open images dataset. The Lambda function pulls randomly images form this data set and uploads to the application for processing.
1. In the top left of the AWS console select **services**
1. In the search box enter *Lambda* and select the service
1. In the Lambda search box eneter *traffic* and hit enter
1. Click into the Lambda function
1. In the top left click **Select a test event** and **Configure test events**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/lambda_test.png">
    </p>
1. For the **Event name** enter test and click create **Create**
1. Now click **test**
1. This should now start prcoessing data and return an *Execution: success* message
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/lambda_success.png">
    </p>

### Review the application serverless processing
1. In the top left of the AWS console select **services**
1. In the search box enter *Step* and select the service
1. Click into your step function e.g. *Demo-state-machine*
1. Under the executions section you should see a number of successful executions, click into one
1. You can now see the details of the processing that has been performed
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/step_success.png">
    </p>

TODO: EDIT STEP FUNCTION

## Create a glue catalog
Now our serverless application is processing data we will use glue to create a schema over the output so we can start to interogate the enrichment of the data being passed into the application.

1. In the top left of the AWS console select **services**
1. In the search box enter *Glue* and select the service


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
