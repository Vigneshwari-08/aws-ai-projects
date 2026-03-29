import boto3
import json

def lambda_handler(event, context):
    try:
        lam = boto3.client('lambda', region_name='us-east-1')
        response = lam.list_functions()
        functions = [{"function_name": f['FunctionName'],
                      "runtime": f.get('Runtime', 'N/A'),
                      "memory_mb": f['MemorySize'],
                      "last_modified": f['LastModified']}
                     for f in response['Functions']]
        result = {"service": "Lambda", "total_functions": len(functions), "functions": functions} if functions else {"service": "Lambda", "total_functions": 0, "message": "No Lambda functions found"}
        return {
            "messageVersion": "1.0",
            "response": {
                "actionGroup": event.get("actionGroup", "AWSInfraTools"),
                "function": event.get("function", "list_lambdas"),
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
                "function": event.get("function", "list_lambdas"),
                "functionResponse": {
                    "responseBody": {
                        "TEXT": {
                            "body": json.dumps({"error": str(e)})
                        }
                    }
                }
            }
        }