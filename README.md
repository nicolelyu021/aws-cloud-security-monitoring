# AWS Cloud Security Monitoring Dashboard

An enterprise-grade serverless security monitoring solution that provides automated compliance tracking, real-time threat detection, and comprehensive security reporting for AWS infrastructure. This production-ready system delivers continuous visibility into security posture through automated metric collection, intelligent threshold analysis, and proactive alerting.

## Overview

This security monitoring system addresses the critical need for continuous security compliance monitoring in cloud environments. Built using serverless architecture principles, the solution automatically scales to handle varying workloads while maintaining minimal operational overhead. The system continuously tracks security best practices across IAM, S3, EC2, and security groups, providing security teams with actionable insights and immediate notifications when violations are detected.

The architecture leverages AWS managed services to ensure high availability and reliability. EventBridge schedules trigger Lambda functions for automated metric collection, eliminating the need for dedicated infrastructure. All collected metrics are published to CloudWatch for real-time visualization, while comprehensive reports are generated and stored in S3 for historical analysis and audit purposes.

## Architecture

The system follows an event-driven, serverless architecture pattern that ensures scalability and cost-effectiveness. The core orchestration is handled by an AWS Lambda function that is triggered on a scheduled basis by Amazon EventBridge. This Lambda function coordinates metric collection, analysis, alerting, and reporting through a modular codebase structure.

![System Architecture](docs/implementation-design.png)

The architecture diagram above illustrates the complete data flow. The Lambda function serves as the central orchestrator, invoking specialized Python modules for different responsibilities. The metrics collector module queries AWS IAM, EC2, and S3 services to gather security-related data. Collected metrics are then published to CloudWatch for dashboard visualization, analyzed for threshold violations, and used to generate comprehensive reports stored in S3. When security violations are detected, the alert manager sends notifications through SNS to subscribed endpoints.

This design ensures separation of concerns, with each module handling a specific responsibility. The shared utilities module provides common functionality for AWS API interactions, error handling, and logging, promoting code reuse and maintainability.

## Security Metrics

The system monitors four primary metric categories, tracking six key security indicators that align with AWS security best practices. The IAM Security category monitors MFA compliance across all IAM users, identifying accounts that lack multi-factor authentication. The Data Encryption category tracks EBS volume encryption compliance, flagging any unencrypted volumes that could expose sensitive data.

The Exposure Risks category identifies potential data exposure by detecting public S3 buckets and EC2 instances with public IP addresses. Finally, the Network Security category analyzes security group rules to identify risky configurations, such as rules that allow access from anywhere (0.0.0.0/0) or expose sensitive ports.

Each metric is collected using direct API calls through the Boto3 SDK, ensuring accurate and up-to-date information. The metrics are then evaluated against configurable thresholds to determine if security violations have occurred.

## Core Components

### Metrics Collection

The metrics collection module implements comprehensive security checks using AWS APIs. Built with Boto3, the module makes direct API calls to EC2, S3, and IAM services to gather security-related information. The implementation includes robust error handling and logging to ensure reliability even when individual API calls fail. Each security check is implemented as a separate function, making the codebase modular and maintainable.

### Lambda Orchestration

The main Lambda handler serves as the execution engine that coordinates all system operations. When triggered by EventBridge, it first collects metrics from multiple AWS services through the metrics collector module. The collected data is then analyzed against predefined thresholds to identify security risks. Metrics are published to CloudWatch for real-time dashboard visualization, and if violations are detected, alerts are triggered through SNS. Optionally, comprehensive reports can be generated and stored in S3, controlled through environment variable configuration.

### Alert Management

The alert management system implements intelligent threshold-based alerting. Each metric type has configurable thresholds that determine when alerts should be triggered. When violations are detected, the system formats structured alert messages with actionable details and sends them through SNS, enabling multi-channel notifications to email, SMS, or other subscribed endpoints.

### Reporting System

The reporting module generates automated security reports in JSON format. Daily reports provide timestamped snapshots of the current security posture, while weekly reports aggregate data over time to identify trends and patterns. All reports are stored in S3 with date-based organization, enabling easy retrieval and analysis. The reporting functionality is designed to be optional, controlled through environment variables to maintain flexibility.

### Infrastructure as Code

The complete infrastructure is defined in a CloudFormation template, enabling repeatable and version-controlled deployments. The template provisions all necessary AWS resources including an SNS topic for alert notifications, an S3 bucket with encryption enabled for report storage, IAM roles with least-privilege permissions, an EventBridge rule for scheduled execution, and a CloudWatch dashboard with pre-configured widgets for metric visualization.

## Technology Stack

The solution is built entirely on AWS managed services, ensuring high availability and eliminating infrastructure management overhead. Python 3.9+ serves as the runtime for Lambda functions, with the Boto3 SDK providing AWS service integration. Infrastructure is defined using CloudFormation YAML templates, following Infrastructure as Code best practices. The system integrates with AWS Lambda for compute, CloudWatch for monitoring, EventBridge for scheduling, SNS for notifications, S3 for storage, IAM for security, and CloudTrail for audit logging.

## Deployment

Deployment begins with the CloudFormation template, which provisions all necessary AWS resources in a single operation. The template creates the SNS topic, S3 bucket, IAM roles, EventBridge rule, and CloudWatch dashboard. Once the infrastructure is deployed, the Lambda function code is packaged with its dependencies and uploaded to AWS Lambda. Environment variables are configured to specify the SNS topic ARN for alerts and optionally the S3 bucket name for report storage.

The Lambda function is configured to use the IAM execution role created by CloudFormation, which has been granted the minimum permissions necessary for the system to operate. The EventBridge rule triggers the Lambda function on a schedule, typically daily or hourly depending on monitoring requirements. After deployment, the CloudWatch dashboard provides immediate visibility into the collected metrics.

## Monitoring and Observability

The system provides comprehensive observability through multiple channels. CloudWatch dashboards offer real-time visualization of all security metrics, enabling security teams to quickly assess the current security posture. CloudWatch Logs capture detailed execution logs for troubleshooting and audit purposes, with structured logging that facilitates analysis.

SNS notifications provide immediate alerts when security violations are detected, ensuring that security teams are promptly informed of critical issues. The S3 report storage serves as a historical record of security compliance, enabling trend analysis and supporting audit requirements. All API calls are logged through CloudTrail, providing a complete audit trail of system operations.

## Security Best Practices

The implementation follows AWS security best practices throughout. IAM roles are configured with least-privilege principles, granting only the minimum permissions necessary for each component to function. The S3 bucket used for report storage has encryption enabled to protect sensitive security data. SNS topic policies restrict access to authorized subscribers, preventing unauthorized access to alert notifications.

All system operations are logged through CloudTrail, providing a complete audit trail for compliance and security reviews. The codebase includes comprehensive error handling to ensure graceful degradation when individual components fail, preventing system-wide outages from isolated failures.

## Project Context

This project was developed as part of the CMU 95-746 Cloud Security capstone course, demonstrating practical application of cloud security principles and serverless architecture design. The implementation showcases production-ready code with proper error handling, logging, and observability. The system demonstrates Infrastructure as Code principles through the complete CloudFormation template, automated reporting and alerting capabilities, and integration with multiple AWS services.

The modular codebase structure and comprehensive documentation reflect software engineering best practices, making the codebase maintainable and extensible. The system is designed to be easily extended with additional security metrics or enhanced with more sophisticated analysis capabilities.

## Project Structure

The codebase is organized into logical modules that separate concerns and promote maintainability. The metrics collector module handles all security metric collection logic, while the Lambda handler coordinates overall execution. The alert manager implements threshold analysis and notification logic, and the reporting module handles report generation and storage. Shared utilities provide common functionality for AWS interactions, error handling, and logging.

The CloudFormation template defines the complete infrastructure in a single file, enabling version-controlled infrastructure deployments. Documentation and demo materials are organized in dedicated directories, keeping the repository structure clean and navigable.
