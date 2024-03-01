"""
Author: Konrad Soares
Script: Scale UP Webservers

"""
import boto3
import http.client
import time

def wait_for_stack_completion(cf_client, stack_name):
    while True:
        response = cf_client.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        stack_status = stack['StackStatus']
        
        if stack_status.endswith('COMPLETE'):
            print(f"Stack {stack_name} creation completed successfully.")
            break
        elif stack_status.endswith('FAILED') or stack_status.endswith('ROLLBACK'):
            raise Exception(f"Stack {stack_name} creation failed or rolled back.")
        
        print(f"Waiting for stack {stack_name} creation to complete...")
        time.sleep(10)  # Wait for 10 seconds before checking again

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    cf_client = boto3.client('cloudformation')
    
    instance_ids = ['i-03ddf60f0be8e9c31', 'i-0801335a63b258574']
    
    try:
        for instance_id in instance_ids:
            instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
            instance_ip = instance_info.get('PublicIpAddress')
            instance_dns = instance_info.get('PublicDnsName')
            
            if instance_ip:
                instance_url = f'http://{instance_ip}/MyTUDublinApp/'
    
                try:
                    conn = http.client.HTTPConnection(instance_ip)
                    conn.request("GET", instance_url)
                    response = conn.getresponse()
                    
                    if response.status != 200:
                        raise Exception(f"Instance {instance_id} returned HTTP error code {response.status}")
                    
                    print(f"Instance {instance_id} is healthy.")
                    
                except Exception as e:
                    print(f"Error: Instance {instance_id} returned {e}")
                    
                    stack_name = 'webserver-default'
                    template_url = 'https://webserver-templates.s3.amazonaws.com/template.yaml'
                    
                    try:
                        cf_client.create_stack(StackName=stack_name, TemplateURL=template_url)
                        print(f"CloudFormation stack creation initiated for {stack_name}.")
                        wait_for_stack_completion(cf_client, stack_name)
                        
                    except Exception as e:
                        print(f'Error creating CloudFormation stack: {str(e)}')
            
            else:
                print(f'Error: Unable to retrieve IP address or DNS name of instance {instance_id}.')
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }

    return {
        'statusCode': 200,
        'body': 'Health check completed successfully.'
    }
