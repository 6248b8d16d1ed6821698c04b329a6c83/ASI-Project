# Build a Voice Bot Running on AWS (20 min)

In this article, we will discover how to build a voice bot running on AWS and access it using
the POST Method in Python. The project aims to build a voice-controlled virtual assistant like
Siri or Cortana. The algorithm will be running on Amazon Web Services (AWS), enabling us to
access any information on the web with a low internet connection.

## Table of Contents
1. [Create a Layer for Lambda Function](#Create-a-Layer-for-Lambda-Function)
2. [Setup Lambda Function on AWS](#Setup-Lambda-Function-on-AWS)
3. [Create DynamoDB database](#Create-DynamoDB-database)
4. [Setup permission for Lambda](#Setup-permission-for-Lambda)
5. [Create JSON files and get the API keys](#Create-JSON-files-and-get-the-API-keys)
6. [Enable HTTP(S) Endpoint](#Enable-HTTP(S)-Endpoint)
7. [Start chatting with your bot](#Start-chatting-with-your-bot)

## Create a Layer for Lambda Function

In this part, we will create a Layer containing all libraries used in our Lambda function. We will proceed with the following steps:
1. Create a free account on AWS.
2. Go on Amazon S3 and click “Get Started with Amazon S3”.
3. Click on “Create bucket”.
4. Choose “asi-project-functions” under “Bucket name”.
5. Click “Create bucket” at the bottom of the page.
6. Download the 2 zip files below. If the file unzips automatically while downloading, compress it again.
  - [ASI Lambda Layer Library Python 3.9 Part 1](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/1ae454ba9b29b7b619947df3331535cd8d09226d/data/layer/asi_lambda_layer_library_python_3_9_part_1.zip)
  - [ASI Lambda Layer Library Python 3.9 Part 2](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/1ae454ba9b29b7b619947df3331535cd8d09226d/data/layer/asi_lambda_layer_library_python_3_9_part_2.zip)
7. Back in your S3 Bucket, click “Upload” and select both zip files.
8. Follow the steps to upload the zip file.
9. Select the “full-library-python.zip” file and click “Copy URL”.
10. Go on AWS Lambda and click “Get Started with AWS Lambda”.
11. Click on “Layers” in the left panel.
12. Click on “Create Layer”.
13. Name it “asi-project-functions” under Name.
14. Choose “Upload a file from Amazon S3” and paste the link of the “full-librarypython.zip” file.
15. Choose “Python 3.9” under “Compatible runtimes – optional “.
16. Click on “Create”.

## Setup Lambda Function on AWS

We will now build our bot’s command using AWS Lambda. We will proceed with the following steps:
1. Go to AWS Lambda.
2. Click on “Create function”.
3. Choose a name under “Function name”.
4. Choose “Python 3.9” under “Runtime”.
5. Click on the “Create function” at the bottom.
6. Delete the current code below:
```python
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```
7. Paste instead the main Python script available on this page: [ASI Script](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/d9b55be171fb03e27df7b9d19242394b6adc7320/src/main.py).
8. Click on “Deploy”.
9. Click “Add a Layer” in the “Layers” category at the bottom of the page.
10. Choose “Custom Layers”.
11. Select “asi-project-functions” in the dropdown list.
12. Choose the last version.
13. Click on “Add”.

## Create DynamoDB database

In this part, we will create our DynamoDB database to save the default data source. We will proceed with the following steps:
1. Go to Amazon DynamoDB and click “Get Started with DynamoDB”.
2. Click “Create table” in the “Get Started” panel.
3. Define “table_source_data” under “Table name”, “main_param” under “Partition key”, and “details_source” under “Sort key” as shown below.
4. Then, click on “Create table”.
5. Open your table and in the “Actions” dropdown list select “Create item”.
6. Define the “main_param” value as “name_source” and the “details_source” value as “Gemini 1.5 Flash”.
7. Click on “Create item”.
8. Finally, reproduce steps 5 to 7 and define the “main_param” value as “memory”. Click on
“Add new attribute” select “string” and fill “details_source” for the attribute name and “i like
chocolate” for the value. The memory of ASI will be stored in this cell. Your database is now
ready to be used.

## Setup permission for Lambda

In this part, we will allow our Lambda Function to access our Amazon S3 files. We will proceed with the following steps:
1. Go to AWS Identity and Access Management (IAM) and click “Get Started AWS IAM”.
2. Click on “Roles” in the left panel.
3. Click on “Create Role”.
4. Select “Lambda” under “Common use cases”.
5. Search for “AmazonS3FullAccess” and “AmazonDynamoDBFullAccess” and select them.
6. Click “Next”.
7. Define “Role Name”.
8. Click “Create Role”.
9. Go back to your Lambda Function.
10. Go to “Configuration” and click “Permissions” in the left panel.
11. Click “Edit” in the “Execution role” panel.
12. Select our newly created role under “Existing role” at the bottom of the page.
13. Finally, click on “Save”.

## Create JSON files and get the API keys

In this part, we will create two JSON files containing our secret keys and parameters. We will proceed with the following steps:
1. To begin, download the following [config_params.json](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/5a51bea404ddadf7a96d8f7cd8b09fee1d2d0010/config/config_params.json) and [config_credentials.json](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/5a51bea404ddadf7a96d8f7cd8b09fee1d2d0010/config/credentials/config_credentials.json) files.
2. Get a free WolframAlpha API key, ChatGPT API key, Gemini, Google Maps, and other services you wish to access and add them to the JSON instead of ######.
3. If you wish to use Telegram, add your Telegram ID or phone number in the JSON instead of ######;
4. Go to Amazon S3.
5. Click on the “asi-project-functions” bucket, “Upload” and, “Add files”.
6. Select “config_params.json” and “config_credentials.json”.
7. Click on upload.

## Enable HTTP(S) Endpoint

The last step to build a Chatbot running on AWS is to enable the HTTP(S) endpoint to access the function via the POST Method. We will proceed in the following way:
1. Go back to your lambda function.
2. In the “Configuration” panel, click on “Function URL” and “Create function URL”.
3. Choose “None” under “Auth type”. We will integrate an authentication system directly within the ASI algorithm.
4. Finally, save the URL under “Function URL”.

## Start chatting with your bot

You can now set up a simple front-end tool to send POST requests to your endpoint. For example, an iPhone user can use the Shortcuts app. Here is how to proceed:

1. Open the Shortcuts app on your iPhone.
2. Reproduce the steps below for:
  - Chatbot

<p align="center">
  <img src="https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/9042f68aa2f2a21501fde7091fa8053ef4542faa/assets/images/Shortcuts%20iPhone%20Chat%20Bot.png" alt="ASI Project Architecture" width="500"/>
</p>
       
  - Voicebot

<p align="center">
  <img src="https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/9042f68aa2f2a21501fde7091fa8053ef4542faa/assets/images/Shortcuts%20iPhone%20Voice%20Bot.png" alt="ASI Project Architecture" width="500"/>
</p>

3. Start discussing with your new bot and customize it as you wish!










