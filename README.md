# ☁️ AWS Orphan Resource Hunter (FinOps Bot)

![CI Status](https://github.com/emredogan-cloud/Cloud-Formation-Project/actions/workflows/ci.yml/badge.svg)

![AWS](https://img.shields.io/badge/AWS-Serverless-orange) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/License-MIT-green)

This project is an **Event-Driven Serverless Application** designed to optimize AWS costs by automatically detecting unused (orphan) EBS volumes and alerting the engineering team via SNS (Email).

## 🏗️ Architecture

The solution leverages pure **Infrastructure as Code (IaC)** using AWS SAM.

1.  **Amazon EventBridge:** Triggers the Lambda function on a daily schedule (Cron).
2.  **AWS Lambda (Python):** Scans the EC2 region using `boto3` pagination to find `available` volumes.
3.  **Amazon SNS:** Sends a notification alert if any orphan resources are detected.

## 🚀 Features

* **Automated Scanning:** Runs daily at 09:00 UTC.
* **Cost Optimization:** Identifies resources wasting money (`available` EBS volumes).
* **Scalable:** Uses `boto3` paginators to handle thousands of volumes.
* **Secure:** Follows "Least Privilege" principles (only `ReadOnly` access).
* **IaC:** Fully deployed via AWS SAM template.

## 🛠️ Installation & Deploy

Prerequisites:
* AWS CLI & SAM CLI installed.
* Python 3.12+

```bash
# 1. Clone the repo
git clone [https://github.com/emredogan-cloud/aws-orphan-hunter.git](https://github.com/emredogan-cloud/aws-orphan-hunter.git)

# 2. Build the application
sam build

# 3. Deploy (You will be asked for your Email address)
sam deploy --guided

Tech Stack
  Compute: AWS Lambda
  IaC: AWS SAM (CloudFormation)
  Language: Python 3.12 (Boto3 SDK)
  Notifications: Amazon SNS

 License
MIT License
