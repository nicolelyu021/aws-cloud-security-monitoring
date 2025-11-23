"""
Alert Manager Module
Contains SNS alert logic for threshold violations
Owner: Nicole (Automation & Alert Engineer)
"""

import boto3
import os
import json
import sys
from typing import Dict, List

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.aws_helpers import get_boto3_client, handle_error


def check_thresholds_and_alert(findings: Dict[str, any]) -> List[str]:
    """
    Analyzes findings against thresholds and triggers alerts.
    
    IMPORTANT: The 'findings' dictionary must have these exact keys from Alejandro's metrics_collector:
    - 'public_s3_buckets': List[str]
    - 'mfa_compliance': Dict[str, List[str]] with 'compliant' and 'non_compliant' keys
    - 'security_groups': List[str]
    - 'cloudtrail_status': Dict[str, bool]
    - 'failed_logins': int
    
    Args:
        findings: Dictionary of collected security metrics from collect_security_metrics()
        
    Returns:
        List of detected risk descriptions (strings)
    """
    risks = []
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    if not sns_topic_arn:
        handle_error(Exception("SNS_TOPIC_ARN environment variable not set"), "check_thresholds_and_alert")
        return risks
    
    # Check for public S3 buckets
    if findings.get('public_s3_buckets') and len(findings['public_s3_buckets']) > 0:
        risk_msg = f"ALERT: {len(findings['public_s3_buckets'])} public S3 bucket(s) detected: {', '.join(findings['public_s3_buckets'])}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Public S3 Buckets Detected",
            message=risk_msg
        )
    
    # Check for MFA non-compliance
    mfa_compliance = findings.get('mfa_compliance', {})
    non_compliant = mfa_compliance.get('non_compliant', [])
    if non_compliant and len(non_compliant) > 0:
        risk_msg = f"ALERT: {len(non_compliant)} IAM user(s) without MFA: {', '.join(non_compliant)}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: MFA Non-Compliance Detected",
            message=risk_msg
        )
    
    # Check for risky security groups
    if findings.get('security_groups') and len(findings['security_groups']) > 0:
        risk_msg = f"ALERT: {len(findings['security_groups'])} security group(s) with risky rules (0.0.0.0/0): {', '.join(findings['security_groups'])}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Risky Security Groups Detected",
            message=risk_msg
        )
    
    # Check CloudTrail status
    cloudtrail_status = findings.get('cloudtrail_status', {})
    if cloudtrail_status:
        non_logging_trails = [trail for trail, is_logging in cloudtrail_status.items() if not is_logging]
        if non_logging_trails:
            risk_msg = f"ALERT: {len(non_logging_trails)} CloudTrail(s) not logging: {', '.join(non_logging_trails)}"
            risks.append(risk_msg)
            send_alert(
                subject="Security Alert: CloudTrail Not Logging",
                message=risk_msg
            )
    
    # Check for excessive failed logins (threshold: > 10)
    failed_logins = findings.get('failed_logins', 0)
    if failed_logins > 10:
        risk_msg = f"ALERT: {failed_logins} failed login attempts detected in last 24 hours (threshold: 10)"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Excessive Failed Login Attempts",
            message=risk_msg
        )
    
    return risks


def send_alert(subject: str, message: str):
    """
    Sends alert via SNS.
    
    Args:
        subject: Alert subject line
        message: Alert message body
    """
    try:
        sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
        if not sns_topic_arn:
            handle_error(Exception("SNS_TOPIC_ARN environment variable not set"), "send_alert")
            return
        
        sns = get_boto3_client('sns')
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject=subject,
            Message=message
        )
    except Exception as e:
        handle_error(e, "send_alert")

