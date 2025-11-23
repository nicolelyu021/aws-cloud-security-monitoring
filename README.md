# AWS Cloud Security Monitoring

## Project Overview

This project implements a Security Monitoring Dashboard for MedTech's AI infrastructure, providing automated tracking of security metrics, real-time alerts, and comprehensive reporting capabilities. The solution follows AWS Well-Architected Framework principles and automates security compliance monitoring.

## Project Scope

This solution implements **Option C: Security Monitoring Dashboard** with the following capabilities:
- Track 3-5 security metrics (e.g., public S3 buckets, IAM MFA compliance, security group rules, CloudTrail status)
- CloudWatch dashboard visualization
- Automated alerts on threshold violations
- Daily/weekly summary reports

## Team Structure

### Alejandro - Infrastructure & Metrics Architect
- Define 3-5 security metrics to track
- Create CloudWatch Metrics and Logs groups
- CloudFormation templates for infrastructure setup
- Architecture diagrams

### Nicole - Automation & Alert Engineer
- Lambda function for metric collection and analysis
- EventBridge/CloudWatch Alarms integration
- SNS notification workflows
- Alert management logic

### Kelly - Reporting & Visualization Lead
- Automated daily/weekly summary reports
- S3 storage for aggregated logs
- CloudWatch dashboard visuals
- Final presentation deck

## Project Structure

```
aws-cloud-security-monitoring/
├── src/
│   ├── metrics_collector/
│   │   └── metrics_collector.py          # Collects security metrics via boto3
│   ├── cloudformation/
│   │   └── dashboard_setup.yaml          # Infrastructure as Code (CloudWatch, SNS, IAM, S3)
│   ├── lambda_handler/
│   │   ├── lambda_handler.py             # Main Lambda function entry point
│   │   └── alert_manager.py              # SNS alert logic and threshold management
│   ├── reporting/
│   │   ├── report_generator.py            # Generates JSON/CSV summary reports
│   │   └── email_sender.py               # Formats and sends reports via SNS/SES
│   └── utils/
│       └── aws_helpers.py                # Shared helper functions (boto3, logging, error handling)
├── docs/
│   ├── architecture_diagram.png           # Visual representation of workflow
│   └── metrics_table.xlsx                # Metrics documentation
├── presentation/
│   └── capstone_slides.pptx              # Final presentation deck
├── demo/
│   └── demo_walkthrough.md               # Step-by-step demo script
└── README.md

```

## Key Components

### Metrics Collection
The `metrics_collector.py` module implements security checks for:
- Public S3 bucket detection
- IAM MFA compliance status
- Security group rule analysis
- CloudTrail logging status
- Failed login attempts

### Lambda Function
The main Lambda handler orchestrates:
1. Metric collection from AWS services
2. Threshold analysis and risk assessment
3. Alert triggering via SNS
4. Metric publishing to CloudWatch

### Alerting System
Automated alerts are triggered when:
- Security metrics exceed defined thresholds
- Critical security findings are detected
- Compliance violations occur

### Reporting
Automated reports include:
- Daily summary of security metrics
- Weekly aggregated compliance status
- Trend analysis and recommendations

## Deployment

### Prerequisites
- AWS CLI configured with appropriate credentials
- Python 3.9+ (for Lambda functions)
- CloudFormation or SAM CLI for infrastructure deployment

### Setup Steps
1. Deploy infrastructure using CloudFormation template
2. Configure SNS topic subscriptions (email/Slack)
3. Deploy Lambda function with required IAM permissions
4. Set up EventBridge rule for scheduled execution
5. Configure CloudWatch dashboard

## AWS Services Used

- **AWS Lambda**: Core automation engine
- **Amazon CloudWatch**: Metrics, logs, and dashboards
- **Amazon EventBridge**: Scheduled execution triggers
- **Amazon SNS**: Alert notifications
- **Amazon S3**: Report storage
- **AWS IAM**: Security and access control
- **AWS CloudFormation**: Infrastructure as Code

## Security Considerations

- Least privilege IAM roles for Lambda execution
- Encrypted S3 buckets for report storage
- Secure SNS topic policies
- CloudTrail logging for audit trails
- Error handling and retry logic

## Deliverables

1. **Code Repository**: Complete implementation with all modules
2. **Infrastructure Templates**: CloudFormation/SAM deployment files
3. **Documentation**: Architecture diagrams and metrics documentation
4. **Presentation**: 10-12 slide deck with demo walkthrough
5. **Demo**: Live or screenshot-based demonstration

## Timeline (2 Weeks)

- **Week 1:**
  - Infrastructure setup (CloudFormation) and metrics collection implementation
  - Lambda automation and alerting implementation
  - Initial integration testing

- **Week 2:**
  - Reporting and visualization implementation
  - Integration testing, bug fixes, and documentation
  - Presentation preparation and final demo

