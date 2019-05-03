# Overview
This lab demonstrates how to build a serverless data processing pipeline to enrich data, catalog it and run add hock queries and reporting.

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
    ```cp -R aws-service-demos/codepipeline/exampleDeployment/* serverlessdataprocessin/```
1. On your local computer checkin the changes and push the application e.g.
    ```cd serverlessdataprocessin/ && git add * && git commit -m 'inital code deployment && git push**```

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
