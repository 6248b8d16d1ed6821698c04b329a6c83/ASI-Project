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
  - [asi_lambda_layer_library_python_3_9_part_2.zip](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/1ae454ba9b29b7b619947df3331535cd8d09226d/data/layer/asi_lambda_layer_library_python_3_9_part_2.zip)
