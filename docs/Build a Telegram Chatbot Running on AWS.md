# Build a Telegram Chatbot Running on AWS (30 min)

In this article, we will discover how to build a Telegram Chatbot running on AWS in Python.
The algorithm will be running on Amazon Web Services (AWS), enabling us to access any
information on the web with a low internet connection.

## Table of Contents
1. [Setup Telegram bot](#Setup-Telegram-bot)
2. [Create a Layer for Lambda Function](#Create-a-Layer-for-Lambda-Function)
3. [Setup Lambda Function on AWS](#Setup-Lambda-Function-on-AWS)
4. [Create DynamoDB database](#Create-DynamoDB-database)
5. [Setup permission for Lambda](#Setup-permission-for-Lambda)
6. [Create JSON files and get the API keys](#Create-JSON-files-and-get-the-API-keys)
7. [Setup API Gateway on AWS](#Setup-API-Gateway-on-AWS)
8. [Setup the Webhook](#Setup-the-Webhook)
9. [Conclusion](#Conclusion)

## Setup Telegram bot

In this part, we are going to build a Telegram bot. We will proceed with the following steps:
1. Install the Telegram Messenger app on your smartphone and create an account if you don’t already have one.
2. Look for @BotFather in the search bar.
3. Click on “Start”.
4. Choose “/newbot”.
5. Choose a name for your bot.
6. Choose a username for your bot. It can be the same as the name but must end with “bot”.
7. Save the token to access the HTTP API. We will need it later.
8. You can access our bot by clicking on the address starting with “t.me/” + your bot name.


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
  - Optional: You can create your personalized zip file by learning [How To Import Python Libraries In AWS Lambda](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/b3ed7c57731d5ef59162c127a0e99006c97cdd25/docs/Import%20Python%20Libraries%20In%20AWS%20Lambda.md).
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
14. Send a message to your Bot on Telegram.
15. Back on your lambda function, go to the “Monitor” category and click on “View
CloudWatch logs”.
16. Click on the most recent “Log streams”.
17. Your Telegram ID is in "message" -> "from" -> "id" as shown below.

```json
{
  "update_id": 1234567891,
  "message": {
    "message_id": 3,
    "from": {
      "id": 9876543219, // this is your Telegram ID
      "is_bot": false,
      "first_name": "John",
      "last_name": "Doe",
      "language_code": "en"
    },
    "chat": {
      "id": 9876543219,
      "first_name": "John",
      "last_name": "Doe",
      "type": "private"
    },
    "date": 1680448807,
    "text": "Hello World!"
  }
}
```

19. Save this Telegram ID. We will need it later.

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
3. Add your Telegram API Key saved in step 7 of the category “Setup telegram bot” in the
JSON instead of #####.
4. Add your Telegram ID saved in step 19 of the category “Setup Lambda Function on AWS”
in the JSON instead of #####.
5. Go to Amazon S3.
6. Click on the “asi-project-functions” bucket, “Upload” and, “Add files”.
7. Select “config_params.json” and “config_credentials.json”.
8. Click on upload.

## Setup API Gateway on AWS

In this part, we will connect our Telegram bot to AWS using API Gateway. We will proceed with the following steps:

1. Go to Amazon API Gateway and click “Get Started with Amazon API Gateway”.
2. In the “APIs” section, click “Create API”.
3. Under “Choose an API type” and “HTTP API” click “Build”.
4. Click “Add integration”.
5. Choose “Lambda” under “Integrations”.
6. Choose your bot lambda function under “Lambda function”.
7. Choose an API name under “API name”.
8. Click “Next”.
9. Choose “POST” under “Method”.
10. Click “Next” two times.
12. Click “Create”.
13. Save the API's URL shown under “Invoke URL”.
14. Add your bot name at the end of the API's URL, separated with an “/” as shown in the
“Develop” -> “Routes” category. The full URL should look like this: https://sl5ssr93v1.executeapi.
us-west-2.amazonaws.com/asi-bot-test.
15. Save the full URL. We will need it later.

## Setup the Webhook

In this part, we are going to create the telegram Webhook. This will link our Telegram Bot with
our API Gateway. This is the final step to build a Telegram ChatBot running on AWS. We will
proceed with the following steps:

1. Complete the Telegram Webhook URL. To proceed, replace [telegram-token] in the
following URL: https://api.telegram.org/bot[telegram-token]/setwebhook. We saved the
token in step 7 of the category “Setup telegram bot”. The result should look like this: https://api.telegram.org/bot8753086164:BBEeIJEAGRtN_K3lZIJHppNAUVdWqBUCIKI/setwebhook
2. We will set up the webhook using Postman. To begin, download the Postman app and sign
up for free.
3. In the dropdown list, choose “POST”.
4. Paste the full Telegram URL created in step 1 in the space “Enter URL or paste text”.
5. In the “Body” category, check “form-data”.
6. Enter “url” under “KEY” and paste the full API URL saved at step 15 of the category “Setup
API Gateway on AWS” under “VALUE”.
6. Click on “Send”.
7. The result should look like the screenshot below



8. The webhook is now set up. We can close Postman.
9. Our Telegram Bot should now be answering our messages.

## Conclusion
In this article, we have learned how to build a Telegram Chatbot running on AWS for free. This
Bot runs on AWS, enabling a high level of security and reliability at a cheap cost.
   
