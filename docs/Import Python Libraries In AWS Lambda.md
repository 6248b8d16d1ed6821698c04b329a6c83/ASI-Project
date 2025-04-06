# How To Import Python Libraries In AWS Lambda?

This article will explore how to import Python libraries in AWS Lambda. It can be helpful if you want to add extra features to your virtual assistant ASI.

## Table of Contents
1. [What is AWS Lambda?](#What-is-AWS-Lambda?)
2. [How to Create a Layer for Lambda Function](#How-to-Create-a-Layer-for-Lambda-Function)
3. [Conclusion](#Conclusion)

## What is AWS Lambda?

AWS Lambda is a serverless computing service by Amazon Web Services that lets you run
code without managing servers. It executes code in response to events like data changes in
S3 or HTTP requests via API Gateway. Key features include automatic scaling, event-driven
execution, and a pay-per-use model, charging only for the number of requests and
execution time. This service simplifies application deployment and management, allowing
developers to focus on writing code rather than handling infrastructure. Now that we know
more about AWS Lambda. Let’s start to create a Layer that will contain our Python libraries.

## How to Create a Layer for Lambda Function

We will create a Layer containing all Python libraries used in our Lambda function. We will proceed with the following steps:
1. Create a free account on AWS.
2. Go on Amazon S3 and click “Get Started with Amazon S3”.
3. Click on “Create bucket”.
4. Choose “asi-project-functions” under “Bucket name”.
5. Click “Create bucket” at the bottom of the page.
6. Go on AWS CloudShell and click “Get Started with CloudShell”.
7. Enter the following commands one by one to import libraries required for ASI:
   
```bash
mkdir packages
cd packages
python3 -m venv venv
source venv/bin/activate
mkdir python
cd python
pip install google-generativeai -t .
pip install fuzzywuzzy -t .
pip install wolframalpha -t .
pip install bs4 -t .
pip install CurrencyConverter -t .
pip install openai -t .
pip install gspread -t .
pip install oauth2client -t .
pip install html2text -t .
pip install random2 -t .
pip install wikipedia -t .
pip install cffi -t .
pip install requests==2.28.2 -t .
pip install 'urllib3<2' -t .
pip install boto3==1.26.90 -t .
pip install httpx==0.23.2 -t .
rm -rf *dist-info
cd ..
zip -r full-library-python.zip python
aws s3 cp full-library-python.zip s3://asi-project-functions/
```

Note that the maximum size of an unzipped deployment package is limited to 250 MB. To create our layer, we must delete unused libraries downloaded as dependencies.

8. Back to the Amazon S3 page, check that the full-library-python.zip file appears in the “asi-project-functions” bucket.
9. Select the full-library-python.zip file and click on “Download”. Once downloaded, you can “Delete” it.
10. Open the folder on your computer, unzip it, and delete the numpy & numpy-lib & pandas files. You can then compress the folder again.
12. Click on “Upload” and select your new zip file.
13. Select the full-library-python.zip file and click on “Copy URL”.
14. Go to AWS Lambda and click “Get Started with AWS Lambda”.
15. Click on “Layers” in the left panel.
16. Click on “Create Layer”.
17. Name it “asi-project-functions” under Name
18. Choose “Upload a file from Amazon S3” and paste the link of the full-librarypython.zip file.
19. Choose “Python 3.9” under “Compatible runtimes – optional “.
20. Click on « Create ».
21. Finally, you can return to your lambda function and “Add a Layer” at the bottom of the page. You will need to choose “Custom layers” to be able to select your new layer.

## Conclusion
You now know how to import Python libraries in your AWS lambda function!






