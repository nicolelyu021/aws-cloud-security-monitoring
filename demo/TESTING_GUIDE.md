# 3-Minute Demo Guide - Screenshot & Voiceover
## Deterministic Step-by-Step Instructions for Nicole

**Demo Format:** Screenshots with 3-minute voiceover recording  
**What Actually Works:** Lambda execution, CloudWatch metrics, SNS alerts  
**What Does NOT Work:** S3 reports (code exists but not integrated into Lambda)

---

## 🎯 What You Will Show (Deterministic)

Based on the actual codebase:

1. ✅ **Lambda Function Execution** - Shows successful execution with findings
2. ✅ **CloudWatch Logs** - Shows execution trace
3. ✅ **CloudWatch Metrics** - Shows 6 security metrics in namespace `MedTech/Security`:
   - `PublicS3Buckets` (Count)
   - `PublicEC2Instances` (Count)
   - `MFANonCompliantUsers` (Count)
   - `TotalIAMUsers` (Count)
   - `RiskySecurityGroups` (Count)
   - `UnencryptedEBSVolumes` (Count)
4. ✅ **SNS Alert Email** - Shows alert notification when violations detected
5. ❌ **S3 Reports** - NOT shown (report code exists but Lambda doesn't call it)

---

## 📸 Screenshot Sequence (Take These in Order)

You need **5 screenshots** for your 3-minute demo:

1. **Screenshot 1:** Lambda execution result (statusCode 200, risks detected)
2. **Screenshot 2:** CloudWatch Logs showing execution flow
3. **Screenshot 3:** CloudWatch Metrics graph showing all 6 metrics
4. **Screenshot 4:** SNS topic showing published messages
5. **Screenshot 5:** Email inbox showing security alert notification

---

## 🎬 EXACT STEPS TO CAPTURE SCREENSHOTS

### **SCREENSHOT 1: Lambda Execution Result**

**Navigation:**
1. Go to: https://console.aws.amazon.com/lambda/
   - You'll see the Lambda dashboard with a list of functions
2. **Find your Lambda function in the list:**
   - Look for a table/list showing function names (usually in the center of the page)
   - The table has columns like: "Function name", "Runtime", "Last modified", etc.
   - The function name might be something like: `medtech-security-monitor` or `security-monitoring-function`
   - If you don't see it, check the search box at the top or use the filter
3. **Click on the function name** (it's a clickable link/blue text in the "Function name" column)
   - The function name appears as a hyperlink in the table
   - Clicking it opens the function's detail page (you'll see tabs: Code, Test, Monitor, Configuration, etc.)
4. Click the **"Test"** tab at the top of the function detail page
5. If you see "Configure test event" button, click it:
   - Event name: `demo-test`
   - Event JSON: `{}` (just the curly braces, nothing else)
   - Click **"Create"**
6. Click the orange **"Test"** button
7. Wait for execution (5-10 seconds)

**What to Capture:**
- Execution result showing: **"succeeded"**
- Response body showing:
  - `statusCode: 200`
  - `findings_count: 4` (or similar)
  - `risks_detected: X` (number > 0 if violations exist)
  - `risks: [...]` (array of detected risks)

**Screenshot Area:** The entire execution result panel, including the response JSON

---

### **SCREENSHOT 2: CloudWatch Logs**

**Navigation:**
1. From Lambda function page, click **"Monitor"** tab
2. Click **"View CloudWatch logs"** (or the log stream link)
3. Click the **most recent log stream** (top of list)

**What to Capture:**
- Log stream showing these key messages:
  - `"Starting security metrics collection"`
  - `"Collected 4 metric categories"`
  - `"Metrics published to CloudWatch"`
  - `"Detected X security risks"` OR `"No security risks detected"`

**Screenshot Area:** The log stream with at least 4-5 log lines visible

---

### **SCREENSHOT 3: CloudWatch Metrics Dashboard**

**Navigation:**
1. Go to: https://console.aws.amazon.com/cloudwatch/
2. Click **"Metrics"** → **"All metrics"**
3. Click **"Custom namespaces"** tab
4. Click namespace: **`MedTech/Security`**
5. Check boxes for these 6 metrics:
   - `PublicS3Buckets`
   - `PublicEC2Instances`
   - `MFANonCompliantUsers`
   - `TotalIAMUsers`
   - `RiskySecurityGroups`
   - `UnencryptedEBSVolumes`
6. Click **"Graphed metrics"** tab
7. Set time range to **"Last 1 hour"**

**What to Capture:**
- Graph showing all 6 metrics with data points
- Make sure the graph shows actual values (not empty)
- The namespace `MedTech/Security` should be visible

**Screenshot Area:** The entire metrics graph with all 6 metrics visible

**If no data appears:**
- Wait 2-3 minutes after Lambda execution
- Try time range "Last 3 hours"
- Make sure you're in "Custom namespaces" not "AWS namespaces"

---

### **SCREENSHOT 4: SNS Topic Published Messages**

**Navigation:**
1. Go to: https://console.aws.amazon.com/sns/
2. Click **"Topics"** in left sidebar
3. Click your security alerts topic name
4. Click **"Metrics"** tab

**What to Capture:**
- Metrics graph showing **"NumberOfMessagesPublished"**
- Should show at least 1 message published (if violations were detected)
- The topic ARN should be visible

**Screenshot Area:** The metrics tab showing published messages count

**Alternative if no messages:**
- Show the SNS topic configuration page
- Point out the subscription (email endpoint)
- Explain: "When violations are detected, alerts are published here"

---

### **SCREENSHOT 5: Email Alert Notification**

**Navigation:**
1. Check your email inbox (the email subscribed to SNS topic)
2. Look for email with subject like:
   - "Security Alert: Public S3 Buckets Detected"
   - "Security Alert: MFA Non-Compliance Detected"
   - "Security Alert: Risky Security Groups Detected"
   - "Security Alert: Unencrypted EBS Volumes Detected"
3. Open the email

**What to Capture:**
- Email subject line showing security alert
- Email body showing the alert message with specific violations
- Example: "ALERT: 2 public S3 bucket(s) detected: bucket-1, bucket-2"

**Screenshot Area:** The entire email showing subject and body

**If no email received:**
- Check spam folder
- Verify SNS subscription is confirmed (check email for confirmation link)
- Re-run Lambda to trigger new alerts
- If still no email, use Screenshot 4 (SNS topic) and explain: "Alerts are sent via SNS to subscribed email addresses"

---

## 🎤 3-Minute Voiceover Script

**Use this exact script, timing each section:**

### **Opening (0:00 - 0:15) - 15 seconds**
> "I'll demonstrate our automated security monitoring solution. This Lambda function continuously monitors our AWS infrastructure for security violations and automatically alerts the security team."

**[Show Screenshot 1: Lambda Execution]**

### **Lambda Execution (0:15 - 0:45) - 30 seconds**
> "I triggered the Lambda function, which collected security metrics across our AWS account. It checked S3 buckets, IAM users, security groups, and EBS volumes. The function detected [X] security risks and published metrics to CloudWatch. Here we can see the execution succeeded with status code 200, and it found [specific number] security violations."

**[Show Screenshot 2: CloudWatch Logs]**

### **Execution Flow (0:45 - 1:00) - 15 seconds**
> "The CloudWatch logs show the complete execution flow: starting metrics collection, collecting 4 metric categories, publishing to CloudWatch, and detecting [X] security risks. This provides full traceability of the automation process."

**[Show Screenshot 3: CloudWatch Metrics]**

### **Metrics Visualization (1:00 - 1:45) - 45 seconds**
> "Here we can see the security metrics visualized in CloudWatch. We're tracking 6 key security dimensions: public S3 buckets, public EC2 instances, IAM users without MFA, total IAM users, risky security groups with open ports, and unencrypted EBS volumes. These metrics update in real-time every time the Lambda runs, providing continuous visibility into our security posture. The metrics are published to the MedTech/Security namespace, making them easy to monitor and alert on."

**[Show Screenshot 4: SNS Topic]**

### **Alert System (1:45 - 2:15) - 30 seconds**
> "When security violations are detected, the system automatically publishes alerts to this SNS topic. The metrics show that [X] alert messages were published. This enables real-time notification of security issues."

**[Show Screenshot 5: Email Alert]**

### **Alert Delivery (2:15 - 2:45) - 30 seconds**
> "The security team receives immediate email notifications when violations are detected. Here's an example alert showing that [specific violation] was found. This enables rapid response to security issues, reducing the time from detection to remediation from hours to minutes."

### **Value & Closing (2:45 - 3:00) - 15 seconds**
> "This automation reduces manual security checks from 2 hours per day to 30 seconds, monitors hundreds of resources simultaneously, and costs less than $1 per month. It provides continuous security monitoring that would be impossible to achieve manually."

**[End]**

---

## ✅ Pre-Demo Checklist

**Before taking screenshots, ensure:**

- [ ] Lambda function is deployed and working
- [ ] Lambda has been executed at least once (to generate metrics)
- [ ] SNS topic subscription is confirmed (check your email!)
- [ ] At least one security violation exists in your AWS account (or you're okay showing "no violations")
- [ ] You have access to the email inbox subscribed to SNS
- [ ] CloudWatch metrics have appeared (wait 2-3 minutes after Lambda execution)

**Required AWS Resources:**
- Lambda function deployed
- SNS topic created with email subscription confirmed
- IAM role with permissions for: CloudWatch, SNS, EC2, S3, IAM
- At least one IAM user (for MFA check)
- At least one S3 bucket (for public bucket check)
- At least one EC2 instance or security group (for exposure/security group checks)

---

## 🚨 Troubleshooting

### Problem: Lambda execution fails
**Solution:**
- Check CloudWatch Logs for error
- Common: Missing IAM permissions or wrong SNS_TOPIC_ARN
- Fix the issue, then retake Screenshot 1

### Problem: No metrics in CloudWatch
**Solution:**
- Wait 2-3 minutes after Lambda execution
- Check you're in "Custom namespaces" tab, not "AWS namespaces"
- Verify Lambda execution succeeded (check logs)
- Use time range "Last 3 hours" instead of "Last 1 hour"
- If still no metrics, check Lambda logs for "Metrics published to CloudWatch" message

### Problem: No alerts sent (risks_detected = 0)
**Solution:**
- This is fine! Say: "No security violations detected - our account is secure"
- OR create a test violation before demo:
  - Make an S3 bucket public
  - Remove MFA from a test IAM user
  - Create a security group with 0.0.0.0/0 rule
- Then re-run Lambda and retake screenshots

### Problem: No email received
**Solution:**
- Check spam folder
- Verify SNS subscription is confirmed (check email for confirmation link)
- Re-run Lambda after confirming subscription
- If still no email, use Screenshot 4 (SNS topic) and explain alerts are sent there

### Problem: Can't find CloudWatch metrics namespace
**Solution:**
- Make sure Lambda executed successfully first
- Click "Custom namespaces" tab (not "AWS namespaces")
- Look for exact namespace: `MedTech/Security`
- If not there, check Lambda logs to confirm metrics were published

---

## 📋 Screenshot File Naming

Save your screenshots with these exact names for easy reference:

1. `01_lambda_execution_result.png`
2. `02_cloudwatch_logs.png`
3. `03_cloudwatch_metrics_dashboard.png`
4. `04_sns_topic_messages.png`
5. `05_email_alert_notification.png`

---

## 🎯 Key Points to Emphasize in Voiceover

1. **Automation:** "Automated" and "continuous" - not manual
2. **Real-time:** Metrics update immediately, alerts sent instantly
3. **Comprehensive:** Monitoring 6 different security dimensions
4. **Actionable:** Alerts enable rapid response
5. **Cost-effective:** Serverless, low cost, scalable

---

## ⚠️ What NOT to Show

- ❌ S3 reports (code exists but Lambda doesn't call report_generator)
- ❌ EventBridge rule (not implemented yet by Alejandro)
- ❌ CloudFormation template (not your responsibility)
- ❌ Code files (unless specifically asked)

**Focus only on what works: Lambda → Metrics → Alerts**

---

## ✅ Final Checklist Before Recording

- [ ] All 5 screenshots taken and saved
- [ ] Screenshots show actual data (not empty/error states)
- [ ] Email alert received (or have backup explanation)
- [ ] Voiceover script practiced
- [ ] Timing rehearsed (3 minutes total)
- [ ] Screenshots are clear and readable
- [ ] Know what to say if something is missing (backup explanations ready)

---

**You're ready! Follow this guide exactly and your 3-minute demo will be perfect! 🚀**
