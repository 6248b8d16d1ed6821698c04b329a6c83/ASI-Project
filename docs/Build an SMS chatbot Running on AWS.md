# Build an SMS chatbot Running on AWS (30 min)

In this article, we will discover how to build an SMS Chatbot running on AWS in Python. The algorithm will be running on Amazon Web Services (AWS), enabling us to access any information on the web without an internet connection.

## Table of Contents
1. [Setup Twilio number](#Setup-Twilio-number)
2. [Create a Layer for Lambda Function](#Create-a-Layer-for-Lambda-Function)
3. [Setup Lambda Function on AWS](#Setup-Lambda-Function-on-AWS)
4. [Setup permission](#Setup-permission)
5. [Create JSON files and get the API key](#Create-JSON-files-and-get-the-API-key)
6. [Setup API Gateway on AWS](#Setup-API-Gateway-on-AWS)
7. [Setup your webhook URL on Twilio](#Setup-your-webhook-URL-on-Twilio)
8. [Bonus: Use SMS Notification for Outbound Message](#Bonus-Use-SMS-Notification-for-Outbound-Message)
9. [Conclusion](#Conclusion)

## Setup Twilio number

In this part, we will buy and set up our Twilio number. We will proceed with the following steps:
1. Create a free account on Twilio.
2. Once on the console, click on “# Phone Number” -> “Manage” -> “Active Numbers”.
3. Click on “Buy a number”.
4. Choose a phone number from a country supporting the “SMS” capability. Choose
carefully to confirm your personal phone number can send A2P SMS to the chosen
country for a low price. The price you will pay per SMS will depend on your mobile plan, as explained below.  
- Example 1: I have a US personal phone number, and my mobile operator is Verizon. I can
choose a US Twilio number. US Twilio phone numbers are allowed to send A2P SMS and cost
$1.15 per month. All SMS sent to this number from my US number from the USA is free as part
of my plan.  
- Example 2: I have a French personal phone number, and my mobile operator is Free Mobile.
French Twilio numbers are not allowed to send A2P SMS (reason here). Thus, my cheapest
option is to choose a number from Sweden. Swedish Twilio numbers can send SMS
and cost $3 per month. In addition, each SMS I will send to this phone number from my
French phone numbers from France will cost me 0.07€ as part of my plan.
5. You may have to “Upgrade” your account to buy a phone number depending on the
country you choose.

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
In this part, we are going to build our bot’s command using AWS Lambda. We will proceed
with the following steps:
1. Go on AWS Lambda.
2. Click on “Create function”.
3. Select “Use a blueprint”.
4. Under “Blueprint name” look for “microservice-http-endpoint-python”.
5. Choose a name under “Function name”.
6. Click on “Remove” the “API Gateway trigger”.
7. Choose “Python 3.9” under “Runtime”.
8. Click on the “Create function” at the bottom.
9. Delete the current code below:
```python
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```
10. Paste instead the main Python script available on this page: [ASI Script](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/d9b55be171fb03e27df7b9d19242394b6adc7320/src/main.py).
11. Delete the current "part 3" of the script as shown below:

```python
## Part 3: Run the whole script with the input
def lambda_handler(event, context):
    # The API support call from Telegram and POST method.
    ## POST method should contain same auth as Telegram in body as JSON string.
    try:
        print(event)
        body=json.loads(event['body'])
        """
        try:
            # Start with Telegram user
            print('Trying Telegram Method')
            # filter to allow only main user
            chat_id=body['message']['chat']['id']
            secret_telegram = get_json_file('config_credentials.json')['telegram']
            url = f'https://api.telegram.org/bot{secret_telegram}/sendMessage'
            allowed_user = get_json_file('config_credentials.json')['telegram_user']
            first_name = body['message']['chat']['first_name']
            
            if chat_id == allowed_user:
                # run algorithm for allowed user
                message_part=body['message'].get('text')
                data = {'url': message_part}
                message_answer = mainScript(message_part, first_name)
                payload = {'chat_id': chat_id,
                            'text': message_answer}
                r = requests.post(url,json=payload)
                return  {"statusCode": 200}
            else:
                message_answer = f"Sorry {first_name} but you do not have access to this bot. Send a message to the owner to get access."
                payload = {'chat_id': chat_id,
                            'text': message_answer}
                r = requests.post(url,json=payload)
                return  {"statusCode": 200}
        
        except:
        """
        # else POST request
        print('Trying POST Method')
        # filter to allow only main user
        chat_id=body['id']
        allowed_user = get_json_file('config_credentials.json')['telegram_user']
        first_name = body['first_name']
        
        if chat_id == allowed_user:
            # run algorithm for allowed user
            message_part=body['message']
            message_answer = mainScript(message_part, first_name)
            return  {"statusCode": 200, 'body': json.dumps(message_answer)}
        
        else:
            return  {"statusCode": 400, 'body': json.dumps("Something went wrong with the POST request. Make sure you enter all parameters")}
        
    except:
        return  {"statusCode": 400, 'body': json.dumps("Something went wrong.")}
```

12. Replace it with the following code:

```python
## Part 3: Run the whole script with the input
def lambda_handler(event, context):
  print(event)
  message_part = event['Body']
  phone_number = event['From']
  allowed_user = get_json_file('config_credentials.json')['sms_user']
  first_name = 'John'

  if phone_number == allowed_user:
    # send message if user allowed
    message = mainScript(message_part, first_name)
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\'<Response><Message><Body>{}</Body></Message></Response>'.format(message)
  else:
    message = "Sorry, but you do not have access to this bot. Send a message to the owner to get access."
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\'<Response><Message><Body>{}</Body></Message></Response>'.format(message)
```

8. Click on “Deploy”.
9. Click “Add a Layer” in the “Layers” category at the bottom of the page.
10. Choose “Custom Layers”.
11. Select “asi-project-functions” in the dropdown list.
12. Choose the last version.
13. Click on “Add”.

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
3. Add your phone number in "sms_user" and replace “+” with “%2B” in the json instead of “#####”. Your phone number should look like this: “%2B33612345678”.
4. Go to Amazon S3.
5. Click on the “asi-project-functions” bucket, “Upload” and, “Add files”.
6. Select “config_params.json” and “config_credentials.json”.
7. Click on upload.

## Setup API Gateway on AWS

In this part, we will build the API Gateway to connect our Lambda function to our Twilio phone number. We will proceed with the following steps:
1. Go to Amazon API Gateway and click “Get Started with Amazon API Gateway”.
2. In the “APIs” section, click “Create API”.
3. Under “Choose an API type” and “REST API” click on “Build”.
4. Choose an “API name” and a “Description”.
5. Click “Create API”.
6. Click “Action” -> “Create Resource”.
7. Choose a “Resource Name” and “Resource Path”.
8. Click “Action” and “Create Method”.
9. Below “Action” select “POST” in the list and click the check mark (✓).
10. In the “Setup” panel, write the name of your “Lambda Function”.
11. Click “Save”.
12. Click “OK” in the “Add Permission to Lambda Function” window.
13. Click on “Integration Request”.
14. Expand “Mapping Templates” at the bottom.
15. Click “Add mapping template”.
16. Insert the following command:
```bash
application/x-www-form-urlencoded
```
17. Click the check mark (✓).
18. Click “Yes, secure this integration” in the “Change passthrough behavior” window.
19. Enter the code below in the editor that appears at the bottom:
    
```velocity
#set($httpPost = $input.path('$').split("&"))
{
#foreach( $kvPair in $httpPost )
  #set($kvTokenised = $kvPair.split("="))
  #if( $kvTokenised.size() > 1 )
    "$kvTokenised[0]" : "$kvTokenised[1]"#if( $foreach.hasNext ),#end
  #else
    "$kvTokenised[0]" : ""#if( $foreach.hasNext ),#end
  #end
#end
}
```

20. Click “Save”.
21. Go back to “Method Execution”.
22. Click on “Integration Response”.
23. Expand the “200” Response and expand “Mapping Templates”.
24. Click on “Add mapping template” and add the code below:

```bash
application/xml
```

25. In the text box, enter the following code:

```bash
$input.path('$')
```

26. Click “Save”.
27. Go back to “Method Execution”.
28. Click “Method Response”.
29. Expand the “200” response.
30. If it’s defined, remove “application/json” under Response Body for 200.
31. Add the following command:

```bash
application/xml
```

32. Select the “Empty” model.
33. Click the check mark (✓).
34. Go back to “Method Execution”.
35. Click “Action” and “Deploy API”.
36. Select “[New Stage]” in “Deployment stage”.
37. Choose a “Stage name” and “Stage description”.
38. Click on the stage name you previously chose and click “POST”.
39. Save the “Invoke URL”. We will need it later.

## Setup your webhook URL on Twilio

In this part, we will connect our Twilio phone number to the API Gateway. We will
proceed with the following steps:
1. Go back to your Twilio Console.
2. Click “Phone Numbers” -> “Manage” -> “Active Numbers”.
3. Click your phone number.
4. Under “Messaging” and “A MESSAGE COMES IN” paste your API Gateway invoke URL.
5. Text your Twilio phone number. You should now receive an answer. Note that for some countries, the answer will arrive in a new discussion.

## Bonus Use SMS Notification for Outbound Message

Most mobile operators offer a free SMS Notification system. By using an API provided by your
operator, you can send SMS notifications without any charge. This means that you only have
to pay for incoming SMS messages, effectively reducing your costs. This method splits the
total cost of querying via SMS in half, as you are only paying for one side of the
communication.

## Conclusion

In this article, we have learned how to build an SMS Chatbot running on AWS. This Bot runs on
AWS and uses a Twilio phone number, enabling a high level of security and reliability at a
cheap cost.
