import boto3
import json

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        buckets = [{"bucket_name": b['Name'], "created_date": str(b['CreationDate'])} 
                   for b in response['Buckets']]
        result = {"service": "S3", "total_buckets": len(buckets), "buckets": buckets} if buckets else {"service": "S3", "total_buckets": 0, "message": "No S3 buckets found"}
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", "AWSInfraTools"),
                "function": event.get("function", "list_s3_buckets"),
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
                "function": event.get("function", "list_s3_buckets"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"error": str(e)})
                        }
                    }
                }
            }
        }