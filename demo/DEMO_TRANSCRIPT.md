# AWS Capstone Demo

## Demo Transcript

Hi I’m Nicole.  
I’ll demo our security monitoring solution. This capstone project shows how automation can strengthen cloud security monitoring in AWS. Our goal was to design a lightweight, serverless system that continuously checks for common security risks, and automatically alerts the team in real time. I will walk you through the 5 key screenshot showing the functionalities.

---

## Screenshot 1 – Lambda Execution Result

**What to show:**  
Lambda function “medtech-security-monitor” run successfully with statusCode: 200.

**Talking Points (≈45 sec):**  
This Lambda function is the core of our automation.  
It’s designed to collect and publish AWS security metrics automatically for the MedTech environment.  
Here you can see I’ve configured it under the function name medtech-security-monitor, using Python 3.10.  
The function uses an IAM role with least-privilege permissions — only the APIs required for CloudWatch, SNS, EC2, S3, and IAM.  
When I trigger the function, it runs successfully, reporting six categories of metrics and confirming no risks were detected.  
This establishes that the automation is working end-to-end and operating with secure, minimal permissions.

---

## Screenshot 2 – CloudWatch Logs

**What to show:**  
Shows detailed Lambda log output — starting metrics collection, publishing results, no risks detected.

**Talking Points (≈40 sec):**  
After execution, all activity is logged automatically to CloudWatch.  
You can see the log messages confirm that the Lambda collected four metric categories and successfully published six metrics to CloudWatch.  
This gives us full observability of our automation pipeline — every step from initialization to metric publishing is recorded.  
This aligns with cloud monitoring best practices — continuous visibility and traceability for serverless security operations.

---

## Screenshot 3 – CloudWatch Metrics Dashboard

**What to show:**  
Displays six metrics in namespace MedTech/Security.

**Talking Points (≈45 sec):**  
Here we can see the CloudWatch Metrics that the Lambda created.  
These represent key security indicators across IAM, EC2, and S3 — such as MFA compliance, public S3 buckets, and risky security groups.  
All six metrics are displayed under the custom namespace MedTech/Security.  
Notice that all values are zero except for one IAM user, which confirms the environment is configured securely.  
This dashboard provides real-time visibility into MedTech’s cloud posture and would allow a SOC analyst to detect deviations immediately.

---

## Screenshot 4 – SNS Topic Configuration

**What to show:**  
Shows topic security-alerts with confirmed email subscription.

**Talking Points (≈40 sec):**  
The alerting mechanism for this system is Amazon SNS.  
Here we see the SNS topic security-alerts with a confirmed email subscription.  
Whenever the Lambda detects a security violation — for example, a public S3 bucket — it publishes a message to this topic.  
SNS then automatically distributes the alert to all subscribed endpoints.  
In this test run, no messages were published because no violations were detected, which actually verifies that our monitoring correctly identifies a secure state.

---

## Screenshot 5 – Email Alert Notification

**What to show:**  
Shows received email: “Security Alert: Public S3 Buckets Detected.”

**Talking Points (≈45 sec):**  
This final screenshot demonstrates the alert system in action.  
To test the end-to-end flow, I intentionally created a public S3 bucket, reran the Lambda, and received this email alert within seconds.  
The alert clearly indicates the issue — one public bucket detected — along with the specific bucket name.  
This validates that the entire pipeline works: detection, CloudWatch logging, metric publishing, and real-time notification through SNS email.  
Once the test was complete, I re-secured the bucket to restore a compliant state.

---

## Closing Line (optional 10–15 sec wrap-up)

In summary, this demo shows how the Security Monitoring Lambda automates continuous compliance in AWS.  
It collects metrics, visualizes them in CloudWatch, and sends real-time alerts via SNS — reducing manual review time and improving MedTech’s cloud security visibility.