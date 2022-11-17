import json

import boto3
from botocore.exceptions import ClientError

def send_email(email,token):

    SENDER = "noreply@prod.sagarmalhotra.me" # must be verified in AWS SES Email
    RECIPIENT = email # must be verified in AWS SES Email

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "User Verification"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
                "http://prod.sagarmalhotra.me/v1/verifyUserEmail?email="+email+"&token="+token
                )     

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def lambda_handler(event, context):
    # TODO implement
    print(event)
    s=event['Records'][0]['Sns']['Message'].replace(" ", "")
    email= s.split("\"email\":\"")[1].split("\",")[0]
    token = s.split("\"token\":\"")[1].split("\"")[0]
    print(email)
    print(token)
    send_email(email,token)