# Overview
This lab demonstrates how to build a serverless data processing pipeline to enrich data, catalog it and run ad-hoc queries and reporting.

The lab also introduces AWS CodePipeline enabling blue/green deployments of the serverless application.

# Prerequisites

Install Git, generate a keypair and add add the public key to your security credentials in AWS. The can be done by following the guide here:

https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html

# Implementation
The follow steps lead you through the process of deploying and testing the application.
## Creating a pipeline to automatically deploy our application
The first step in our development cycle is to implement a codepipeline to automatically test, build and deploy our application.

Doing this via the AWS console can be a time consuming task so we'll first deploy a CloudFormation script which will setup the majority of the pipeline and associated IAM roles and CodeBuild steps.

To do this click on the following link which will open the AWS CloudFormation console and load hte template ready for deployment.

| AWS Region | Short name | |
| -- | -- | -- |
| EU West (Ireland) | eu-west-1 | <a href="https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=serverlessdataprocessing&templateURL=https://s3-eu-west-1.amazonaws.com/aws-shared-demo-cf-templates/codepipeline/code-pipeline.yaml" target="_blank"><img src="images/cloudformation-launch-stack.png"></a> |

1. On the page that opens click **next**
1. Enter a project name e.g. *serverlessdataprocessing* and click **next**
1. Click **next**
1. You may be asked to acknowledge that AWS CloudFormation might create IAM resources with custom names.
    <p align="left">
      <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/cf_iam_perms.png">
    </p>

   If so, check the box.
1. Click **Create Stack**

This will take approximatly 5 minutes to deploy the stack and should result in CREATE_COMPLETE.

<p align="left">
  <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/cf_create_complete.png">
</p>

Once our pipeline is deployed we're going to add an additional stage. This stage will run a CodeBuild job to first execute our unitests before continuing to prepare and deploy the application.

### Add a CodePiple stage for unitesting

Usually this would be deinfed as part of the code that builds the pipeline but we are adding it manually as an oppurtunity to explore CodePipeline and CodeBuild.

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

1. Within the CodePipeline console expand **source** in the left menu and select **repositories**
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
Now our serverless application is processing data we will use glue to create a schema over the output so we can start to interogate the output of the enrichment performed by the application.

1. In the top left of the AWS console select **services**
1. In the search box enter *Glue* and select the service
1. Click **Get Started**
1. In the left hand menu select **Crawlers**
1. Click **Add crawler**
1. Enter *ServerlessDataProcessingOutput* for the **Name** and click **Next**
1. For the **Include path** choose the folder icon to the right and select the Output bucket, e.g. *serverlessdataprocessing-application-outputbucket-10zagh3xz94ss*, click **Next**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/glue_bucket.png">
    </p>
1. Click **Next**
1. When asked if you wish to add more data stores, choose No, and click **Next**
1. Enter *serverlessDataProcessing* for **AWSGlueServiceRole-** and click **Next**
1. Click **Next**
1. Choose to run the crawler on-demand. Click **Next**
1. Click **Add Database** and enter *ServerlessDataProcessing* for the **Database name**
1. Click **Next** and **Finish**
1. Finally click **Run it now?**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/glue_crawler_run.png">
    </p>
1. Wait for the crawler to complete, it usually takes about 2 minutes.
1. Once complete, click **Tables** in the left hand menu to see details about the schema on read created by Glue.
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/glue_tables.png">
    </p>

## Query QuickSight
Now we have a schema over the enriched data we can start to visualise the output.
1. In the top left of the AWS console select **services**
1. In the search box enter *QuickSight* and select the service
    **Note:** You may need to enter an email address here, you can enter a fake one
1. In the top right hand corner select **Ireland** and change the region to **US East (N. Virginia)**
1. Close the pop-up box that appears
1. Now click your username to the right and choose **Manage Quicksight**
1. In the left hand menu click **Account Settings**
1. Click **Add or remove** under the 'Connected Products and Services' header
1. Check **Amazon S3**, select the *Output* bucket and click **Select Buckets**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/qs_buckets.png">
    </p>
1. Check **Athena**
1. Click **Update**
1. In the top right hand corner select **N. Virginia** and change the region to **EU (Ireland)**
1. In the top right click **Manage data**
1. Click **New dataset**
1. Select **Athena** and enter the *serverlessDataprocessingOutput* for the **Data source name**
1. Click Validate to ensure a successful connection
1. Click **Create datasource**
1. Select **serverlessdataprocessing** for the **Database**
1. Click **Use custom SQL** and enter
    ```SELECT 
    labels2.name, labels2.confidence, objectId
    FROM 
    ServerlessDataProcessing.rekognitionimagedetectlabels  CROSS JOIN UNNEST(labels) as t(labels2)
    ```
1. Click **Confirm Query**
1. Click **Visualize**
1. When presented with the visualisation drag **Name** from the left into the box named **AutoGraph**
1. At the bottom of the page click **Pie Chart**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/qs_pie.png">
    </p>
1. Finally click the **other** section of the graph and click **Hide**
    <p align="left">
      <img width="250" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/qs_hide.png">
    </p>
1. On the left select **Filter**
1. Click the **+** symbol next to **Applied Filters** and select **Confidence**
1. Click on the filter **confidence** and change **Equals** to **greater than or equal to** and enter **90** into the entry box. This will now only display information for images where the catagorisation was above 90%. 

## Use Athena to query data
Whilst visualisation is useful it is also helpful to query the data directly with SQL, to do this we'll use Amazon Athena.
1. Visit https://console.aws.amazon.com to return to the AWS Console
1. In the search box enter *Athena* and select the service
1. In the left hand dropdown select **ServerlessDataProcessing** for the **Database**
1. IN the query section center the following code
```SELECT
rekognitionimagedetectlabels.objectid, labels2.name, labels2.confidence, rekognitionimagefacedetection.facedetails, rekognitionimagedetecttext.textdetections
FROM
rekognitionimagedetectlabels  CROSS JOIN UNNEST(labels) as t(labels2)
INNER JOIN serverlessdataprocessing.rekognitionimagefacedetection ON rekognitionimagedetectlabels.objectid=rekognitionimagefacedetection.objectid
INNER JOIN serverlessdataprocessing.rekognitionimagedetecttext  ON rekognitionimagedetectlabels.objectid=rekognitionimagedetecttext.objectid
where labels2.confidence > 98 and labels2.name like '%Human%' order by labels2.confidence desc
```
1. If you are interested you can take the objectid and open the S3 input bucket and download the image to see the image that was analysed

## Demonstrate blue/green
The last stage of the CI/CD process is to demonstrate how we can protect our deployments with automated checks that will use the monitoring we have in place for our application to spot errors that are introduced when we push code and automatically role back. This is often the case where there are conditions that only become apart in production and are too difficult or costly to reproduce in pre-production.

To demonstate this we are going to introduce a breaking change to our application. Code deploy will release the code and then start shifting a percentage of traffic through the new application code. When the new code starts to error CloudWatch will pick up and notify our pipeline that an error has been caused causing our pipeline to fail all traffic back to the old code and mark the deployment as failed.

1. On your local computer open the file **serverlessdataprocessing** repository called **dataType/dataType.py** in an editor
1. Comment in the following lines
```
    if readHead(event) == 'image/jpeg':
        event['Records'][0]['s3']['object']['key'] = 'non-existent-key'
```
1. Add, commit and push the changes to code commit e.g.
```
git add dataType/dataType.py && git commit -m 'Force breaking change' ;  git push
```
1. In the top left of the AWS console select **services**
1. In the search box enter *CodePipeline* and select the service
1. When the change reaches the last stage expand **Deploy** in the left hand menu and click **Deployments**
1. Eventually you will see the deployment start and click the **Deployment ID**
1. You will now see the traffic starting to push a percentage of users onto the the code
    <p align="left">
      <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/codedeploy_success.png">
    </p>
1. Eventually you will see the process fail and the traffic will revert 100% to the original code whilst codepipeline marks the deployment as failed
    <p align="left">
      <img width="500" src="https://github.com/charliejllewellyn/aws-serverless-dataprocessing/blob/master/images/codedeploy_rollback.png">
    </p>
