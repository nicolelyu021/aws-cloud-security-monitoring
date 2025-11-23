# Demo Walkthrough Script

## Overview
This document provides a step-by-step guide for demonstrating the Security Monitoring Dashboard solution.

## Pre-Demo Setup
1. Ensure CloudFormation stack is deployed
2. Verify SNS topic subscription is confirmed
3. Have test AWS resources ready (S3 buckets, IAM users, etc.)

## Demo Flow

### Step 1: Introduction (1 minute)
- Explain the problem: Manual security monitoring is time-consuming
- Show current state: No automated monitoring

### Step 2: Architecture Overview (2 minutes)
- Display architecture diagram
- Explain components: Lambda, CloudWatch, SNS, S3
- Show EventBridge schedule

### Step 3: Trigger Lambda Execution (2 minutes)
- Manually invoke Lambda function OR
- Show EventBridge rule triggering automatically
- Display CloudWatch Logs showing execution

### Step 4: Show Metrics Collection (3 minutes)
- Display CloudWatch Metrics dashboard
- Show collected metrics:
  - Public S3 buckets count
  - MFA compliance percentage
  - Security group violations
  - CloudTrail status
  - Failed login attempts

### Step 5: Demonstrate Alert (2 minutes)
- Create a test violation (e.g., make S3 bucket public)
- Show alert being triggered
- Display SNS notification (email or Slack)

### Step 6: Show Report (2 minutes)
- Display daily summary report in S3
- Show formatted report content
- Explain weekly aggregation

### Step 7: Value Demonstration (2 minutes)
- Show time savings calculation
- Display coverage metrics
- Explain cost implications

## Backup Plan (Screenshot-Based)
If live demo fails, use screenshots showing:
1. CloudWatch dashboard with metrics
2. SNS notification email
3. S3 report file
4. Lambda execution logs

## Key Talking Points
- Automation reduces manual effort from hours to minutes
- Continuous monitoring vs. periodic manual checks
- Cost-effective solution using serverless architecture
- Scalable to monitor hundreds of resources

