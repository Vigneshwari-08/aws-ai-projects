import boto3
import json

def lambda_handler(event, context):
    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        response = ec2.describe_instances()
        instances = []
        for r in response['Reservations']:
            for i in r['Instances']:
                name = next((t['Value'] for t in i.get('Tags', [])
                           if t['Key'] == 'Name'), 'unnamed')
                instances.append({
                    'instance_id': i['InstanceId'],
                    'instance_name': name,
                    'instance_type': i['InstanceType'],
                    'state': i['State']['Name']
                })
        result = {"service": "EC2", "total_instances": len(instances), "instances": instances} if instances else {"service": "EC2", "total_instances": 0, "message": "No EC2 instances found"}
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", "AWSInfraTools"),
                "function": event.get("function", "list_ec2_instances"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps(result)
                        }
                    }
                }
            }
        }
    except Exception as e:
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", "AWSInfraTools"),
                "function": event.get("function", "list_ec2_instances"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"error": str(e)})
                        }
                    }
                }
            }
        }
