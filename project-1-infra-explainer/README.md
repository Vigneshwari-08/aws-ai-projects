# AWS Infra Explainer Agent

An autonomous AI agent built with Amazon Bedrock that inspects your 
AWS account and returns a plain-English summary of all running resources.

## Demo

> "What's currently running in my AWS account?"

**Agent response:**
- EC2: 1 running instance (Linux_instance, t3.micro)
- S3: 2 buckets
- Lambda: 5 functions across Python 3.11, 3.12, 3.14

## Architecture

![Architecture](docs/architecture.png)

The agent uses the **ReAct loop** (Reason → Act → Observe → Reason):
1. User asks a question in natural language
2. Bedrock Agent (Amazon Nova Pro) reasons about which tools to call
3. Agent calls Lambda tools autonomously in sequence
4. Each Lambda queries real AWS APIs via boto3
5. Agent synthesises all results into a plain-English summary

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon Bedrock Agents | Agent orchestration and ReAct reasoning loop |
| Amazon Nova Pro | Foundation model for reasoning |
| AWS Lambda | Tool functions called by the agent |
| IAM | Permissions and roles |
| boto3 | AWS SDK for Python |

## Project Structure
```
project-1-infra-explainer/
├── lambda/
│   ├── list_ec2_instances.py   # Lists EC2 instances
│   ├── list_s3_buckets.py      # Lists S3 buckets  
│   └── list_lambdas.py         # Lists Lambda functions
├── iam/
│   └── bedrock_agent_policy.json  # IAM policy for agent role
├── docs/
│   └── architecture.png        # Architecture diagram
└── README.md
```

## Setup Guide

### Prerequisites
- AWS account (free tier works)
- AWS CLI configured
- Python 3.12+

### Deploy

1. Create IAM role and attach `iam/bedrock_agent_policy.json`
2. Deploy all 3 Lambda functions from `lambda/` folder
3. Create Bedrock Agent with Amazon Nova Pro model
4. Add 3 action groups pointing to each Lambda
5. Prepare and test the agent

### Agent Instructions
```
You are an AWS infrastructure assistant. When asked about what is running 
in an AWS account, you MUST call all three tools: list_ec2_instances, 
list_s3_buckets, and list_lambdas. Summarise the results in a friendly 
readable format grouped by service. Always mention counts and highlight 
anything unusual like stopped instances.
```

## What I Learned

- How Bedrock Agents orchestrate tools using the ReAct pattern
- Setting up IAM permissions for AI agent services
- Using inference profiles for newer foundation models
- Debugging AI agents end to end in AWS Console
- Structuring Lambda functions as agent tools

## Author

Built as part of my AWS AI Practitioner certification learning journey.