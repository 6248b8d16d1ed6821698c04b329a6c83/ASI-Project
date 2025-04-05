# Build a Voice Bot Running on AWS (20 min)

In this article, we will discover how to build a voice bot running on AWS and accessible via
the POST Method in Python. The project aims to build a voice-controlled virtual assistant like
Siri or Cortana. The algorithm will be running on Amazon Web Services (AWS), enabling us to
access any information on the web with a low internet connection. You can also explore the
detailed steps to get more details information on each step.

## Create a Layer for Lambda Function

In this part, we will create a Layer containing all libraries used in our Lambda function. We will proceed with the following steps:
1. Create a free account on AWS.
2. Go on Amazon S3 and click on “Get Started with Amazon S3”.
3. Click on “Create bucket”.
4. Choose “asi-project-functions” under “Bucket name”.
5. Click “Create bucket” at the bottom of the page.
6. Download the 2 zip files below. If the file unzips automatically while downloading, make sure to compress it again.
  - [ASI Lambda Layer Library Python 3.9 Part 1](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/1ae454ba9b29b7b619947df3331535cd8d09226d/data/layer/asi_lambda_layer_library_python_3_9_part_1.zip)
  - [ASI Lambda Layer Library Python 3.9 Part 2](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/1ae454ba9b29b7b619947df3331535cd8d09226d/data/layer/asi_lambda_layer_library_python_3_9_part_2.zip)
7. Back in your S3 Bucket, click on “Upload” and select both zip files.
8. Follow the steps to upload the zip file.
9. Select the “full-library-python.zip” file and click on “Copy URL”.
10. Go on AWS Lambda and click on “Get Started with AWS Lambda”.
11. Click on “Layers” in the left panel.
12. Click on “Create Layer”.
13. Name it “asi-project-functions” under Name.
14. Choose “Upload a file from Amazon S3” and paste the link of the “full-librarypython.zip” file.
15. Choose “Python 3.9” under “Compatible runtimes – optional “.
16. Click on “Create”.

## Setup Lambda Function on AWS

In this part, we will build our bot’s command using AWS Lambda. We will proceed with the following steps:
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
7. Paste instead the main Python script available on this page: ASI Script.
8. Click on “Deploy”.
9. Click on “Add a Layer” in the “Layers” category at the bottom of the page.
10. Choose “Custom Layers”.
11. Select “asi-project-functions” in the dropdown list.
12. Choose the last version.
13. Click on “Add”.

