# AWS Setup Log - Security Monitoring Lambda

This document tracks the AWS infrastructure setup steps required to capture demo screenshots.

# Screenshot 1 Details

## Prerequisites Completed

### 1. Lambda Function Creation
- **Function Name:** `medtech-security-monitor`
- **Runtime:** Python 3.10
- **Architecture:** x86_64
- **Handler:** `lambda_handler.lambda_handler.lambda_handler`
- **Region:** us-east-1 (N. Virginia)

### 2. Code Deployment
- **Package Location:** `src/lambda-deployment.zip`
- **Package Contents:**
  - `lambda_handler/` (lambda_handler.py, alert_manager.py)
  - `metrics_collector/` (metrics_collector.py)
  - `utils/` (aws_helpers.py)
  - `reporting/` (report_generator.py, email_sender.py)
- **Upload Method:** AWS Console → Code tab → Upload from → .zip file

### 3. IAM Role Setup
- **Role Name:** `MedTechSecurityMonitoringRole`
- **Policy Name:** `MedTechSecurityMonitoringPolicy`
- **Policy Permissions:**
  - CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents
  - CloudWatch Metrics: PutMetricData
  - SNS: Publish
  - EC2: DescribeInstances, DescribeVolumes, DescribeSecurityGroups
  - S3: ListAllMyBuckets, GetBucketAcl
  - IAM: ListUsers, ListMFADevices
- **Attachment:** Role attached to Lambda function via Configuration → Permissions

### 4. SNS Topic Setup
- **Topic Name:** `security-alerts`
- **Topic ARN:** `arn:aws:sns:us-east-1:851725219956:security-alerts`
- **Subscription:** Email subscription configured and confirmed
- **Environment Variable:** `SNS_TOPIC_ARN` set in Lambda function

### 5. Environment Variables
- **SNS_TOPIC_ARN:** `arn:aws:sns:us-east-1:851725219956:security-alerts`
- **Location:** Lambda → Configuration → Environment variables

## Setup Steps Summary

1. Created Lambda function via AWS Console
2. Created IAM policy with required permissions (JSON policy)
3. Created IAM role and attached policy
4. Created SNS topic for security alerts
5. Subscribed email to SNS topic and confirmed subscription
6. Packaged Lambda code into zip file
7. Uploaded zip file to Lambda function
8. Set handler path in Lambda runtime settings
9. Attached IAM role to Lambda function
10. Set environment variable for SNS topic ARN

## Key Configuration Details

**Lambda Handler Path:**
```
lambda_handler.lambda_handler.lambda_handler
```
(Format: folder.file.function)

**IAM Policy JSON Location:**
Created via IAM Console → Policies → Create policy → JSON tab

**SNS Topic ARN Format:**
```
arn:aws:sns:REGION:ACCOUNT-ID:TOPIC-NAME
```

## Troubleshooting Notes

**Issue:** Lambda execution failed with AccessDenied for iam:ListUsers
**Solution:** Lambda was using wrong IAM role. Fixed by attaching `MedTechSecurityMonitoringRole` via Configuration → Permissions → Edit

**Issue:** Handler was set to `lambda_function.lambda_handler` (default)
**Solution:** Updated to `lambda_handler.lambda_handler.lambda_handler` via Runtime settings → Edit

**Issue:** No Lambda functions visible in console
**Solution:** Checked correct region (us-east-1) and ensured function was created in that region

## File:
`demo/01_lambda_execution_result.png`


# Screenshot 2 Details

**Location:** CloudWatch Logs → Log groups → `/aws/lambda/medtech-security-monitor` → Most recent log stream

**Key Log Messages Captured:**
- `[INFO] Starting security metrics collection`
- `[INFO] Collected 4 metric categories`
- `[INFO] Published 6 metrics to CloudWatch`
- `[INFO] Metrics published to CloudWatch`
- `[INFO] No security risks detected`

**Navigation Path:**
1. Lambda function → Monitor tab → View CloudWatch logs
2. OR: CloudWatch Console → Logs → Log groups → `/aws/lambda/medtech-security-monitor` → Most recent log stream

## File:
`demo/02_cloudwatch_logs.png`

# Screenshot 3 Details

**Location:** CloudWatch → Metrics → All metrics → Custom namespaces → `MedTech/Security`

**Configuration:**
- Statistic: Average (not "last" - this was key to getting data to display)
- Period: 1 hour
- Time range: Last 3 hours
- Graph type: Line

**Metrics Displayed:**
All 6 security metrics are visible on the graph:
1. `TotalIAMUsers`
2. `PublicS3Buckets`
3. `PublicEC2Instances`
4. `MFANonCompliantUsers`
5. `RiskySecurityGroups`
6. `UnencryptedEBSVolumes`

**Metric Values (Findings):**
- **TotalIAMUsers = 1:** There is 1 IAM user in the account
- **MFANonCompliantUsers = 0:** That user has MFA enabled (no violations)
- **PublicS3Buckets = 0:** No public S3 buckets (no violations)
- **PublicEC2Instances = 0:** No public EC2 instances (no violations)
- **RiskySecurityGroups = 0:** No risky security groups (no violations)
- **UnencryptedEBSVolumes = 0:** All volumes are encrypted (no violations)

**Navigation Path:**
1. CloudWatch Console → Metrics → All metrics
2. Click "Custom namespaces" tab
3. Click namespace: `MedTech/Security`
4. Check all 6 metrics
5. Click "Graphed metrics" tab
6. Set Statistic to "Average" and Period to "1 hour" for all metrics
7. Set time range to "Last 3 hours"

**Troubleshooting Notes:**
- Initially got error "There was an error while trying to get graph data"
- Fixed by changing Statistic from "last" to "Average"
- Fixed by changing Period from "6 hours" to "1 hour"
- Metrics take a few minutes to appear after Lambda execution

## File:
`demo/03_cloudwatch_metrics_dashboard.png`

# Screenshot 4 Details

**Location:** SNS Console → Topics → `security-alerts` → Subscriptions tab

**Navigation Path:**
1. Go to: https://console.aws.amazon.com/sns/
2. Click "Topics" in left sidebar
3. Click topic name: `security-alerts`
4. Click "Subscriptions" tab

**What Was Captured:**
- Topic name: `security-alerts`
- Topic ARN: `arn:aws:sns:us-east-1:851725219956:security-alerts`
- Subscriptions section showing 1 confirmed email subscription
- Subscription status: Confirmed (green checkmark)
- Protocol: EMAIL
- Endpoint: Email address subscribed to topic

**Findings:**
- **NumberOfMessagesPublished = 0:** No alerts were published because no security violations were detected (risks_detected: 0 from Screenshot 1)
- **Subscription Status = Confirmed:** Email subscription is active and ready to receive alerts
- **Alert System Status:** Configured and operational, but no alerts needed due to secure account state

**Note:** The SNS topic page does not have a "Metrics" tab in the current AWS console interface. Instead, the Subscriptions tab was used to show the alert configuration, which is the alternative approach mentioned in the test guide for when no messages are published.

**Demo Explanation:**
"When security violations are detected, the system automatically publishes alerts to this SNS topic. The subscription here shows where alerts are sent - in this case, to my email address. Currently, we see no messages published because no security violations were detected, which demonstrates that our account is secure."

## File:
`demo/04_sns_topic_messages.png`

# Screenshot 5 Details

**Location:** Email inbox (Gmail) - email subscribed to SNS topic

**Navigation Path:**
1. Check email inbox for email subscribed to SNS topic
2. Look for email with subject: "Security Alert: Public S3 Buckets Detected"
3. Open the email

**What Was Captured:**
- Email from: AWS Notifications <no-reply@sns.amazonaws.com>
- Email to: yueninglyu@gmail.com
- Subject: "Security Alert: Public S3 Buckets Detected"
- Email body: "ALERT: 1 public S3 bucket(s) detected: medtech-public-bucket-for-alert-testing-2"
- Timestamp: Wed, Dec 10, 2025 at 11:12 PM
- Unsubscribe link and AWS support information

**Findings:**
- Alert email successfully received after creating test violation
- Subject line clearly indicates security alert type
- Body message shows specific violation: 1 public S3 bucket detected
- Bucket name included in alert: `medtech-public-bucket-for-alert-testing-2`
- Alert system is fully operational and delivers notifications in real-time

**Troubleshooting Process:**

**Issue 1: No alert email received initially**
- **Problem:** Created bucket with "Bucket owner enforced" (ACLs disabled) and made it public via bucket policy
- **Root Cause:** Lambda code checks ACLs for public buckets, not bucket policies. Code at line 57-60 in `metrics_collector.py` uses `s3.get_bucket_acl()` and looks for 'AllUsers' in ACL grants
- **Solution:** Recreated bucket with "ACLs enabled" and made it public via ACL instead of bucket policy

**Issue 2: ACL Edit button grayed out**
- **Problem:** First bucket created with "Bucket owner enforced" setting disabled ACLs
- **Root Cause:** When ACLs are disabled, ACL settings cannot be edited
- **Solution:** Deleted first bucket and created new bucket with "ACLs enabled" selected during creation

**Final Solution:**
1. Created new bucket: `medtech-public-bucket-for-alert-testing-2`
2. Selected "ACLs enabled" (not "Bucket owner enforced") during bucket creation
3. Unchecked all 4 "Block public access" boxes
4. After creation, went to Permissions → Access Control List (ACL) → Edit
5. Under "Public access", checked "Read" for Objects
6. Re-ran Lambda function
7. Received alert email successfully

**Key Learning:**
The Lambda function's `check_exposure()` method only checks ACLs for public buckets, not bucket policies. To trigger alerts for public S3 buckets, the bucket must be public via ACL, which requires ACLs to be enabled during bucket creation.

**Note:** After taking screenshot, the test bucket has been made private again (uncheck "Read" under Public access in ACL) to restore security.

## File:
`demo/05_email_alert_notification.png`

# Requirement Reference

- **Test Guide:** `demo/TESTING_GUIDE.md`

# Current Screenshot Status

- [x] Screenshot 1: Lambda execution result (statusCode: 200, findings_count: 4, risks_detected: 0)
- [x] Screenshot 2: CloudWatch Logs (shows execution flow: Starting security metrics collection, Collected 4 metric categories, Metrics published to CloudWatch, No security risks detected)
- [x] Screenshot 3: CloudWatch Metrics Dashboard (all 6 metrics visible with data points)
- [x] Screenshot 4: SNS Topic Published Messages (topic configuration and subscriptions shown)
- [x] Screenshot 5: Email Alert Notification (actual security alert email received)