"""
Author: Konrad Soares
Script: Destroy Webservers

"""
import boto3

def lambda_handler(event, context):
    stack_name = 'webserver-default'

    client = boto3.client('cloudformation')

    try:
        response = client.delete_stack(StackName=stack_name)
        print("Stack deletion initiated:", response)
    except Exception as e:
        print("Error deleting stack:", str(e))

    return {
        'statusCode': 200,
        'body': 'CloudFormation stack deletion initiated'
    }