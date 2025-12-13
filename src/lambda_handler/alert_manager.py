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
    
    This function checks for common security issues. Adjust thresholds and checks
    based on what metrics Alejandro implements.
    
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
    
    # Check for public S3 buckets (from exposure dict)
    exposure = findings.get('exposure', {})
    public_buckets = exposure.get('public_s3_buckets', [])
    if public_buckets and len(public_buckets) > 0:
        risk_msg = f"ALERT: {len(public_buckets)} public S3 bucket(s) detected: {', '.join(public_buckets)}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Public S3 Buckets Detected",
            message=risk_msg
        )
    
    # Check for public EC2 IPs (from exposure dict)
    public_ec2_ips = exposure.get('public_ec2_IPs', [])
    if public_ec2_ips and len(public_ec2_ips) > 0:
        risk_msg = f"ALERT: {len(public_ec2_ips)} EC2 instance(s) with public IPs detected: {', '.join(public_ec2_ips)}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Public EC2 Instances Detected",
            message=risk_msg
        )
    
    # Check for MFA non-compliance (from mfa_iam dict)
    mfa_iam = findings.get('mfa_iam', {})
    non_compliant_users = mfa_iam.get('non_compliant_users', [])
    if non_compliant_users and len(non_compliant_users) > 0:
        risk_msg = f"ALERT: {len(non_compliant_users)} IAM user(s) without MFA: {', '.join(non_compliant_users)}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: MFA Non-Compliance Detected",
            message=risk_msg
        )
    
    # Check for risky security groups (list of dicts)
    security_groups = findings.get('security_groups', [])
    if security_groups and len(security_groups) > 0:
        sg_ids = [sg.get('SecurityGroupId', 'Unknown') for sg in security_groups]
        risk_msg = f"ALERT: {len(security_groups)} security group(s) with risky rules (0.0.0.0/0): {', '.join(sg_ids)}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Risky Security Groups Detected",
            message=risk_msg
        )
    
    # Check for unencrypted EBS volumes
    unencrypted_volumes = findings.get('encryption', [])
    if unencrypted_volumes and len(unencrypted_volumes) > 0:
        risk_msg = f"ALERT: {len(unencrypted_volumes)} unencrypted EBS volume(s) detected: {', '.join(unencrypted_volumes)}"
        risks.append(risk_msg)
        send_alert(
            subject="Security Alert: Unencrypted EBS Volumes Detected",
            message=risk_msg
        )
    
    # CloudTrail and login_attempts alerts are disabled for presentation
    # Uncomment below to enable:
    # cloudtrail = findings.get('cloudtrail', {})
    # if not cloudtrail.get('cloudtrail_enabled', False):
    #     risk_msg = f"ALERT: CloudTrail logging is NOT enabled. Active trails: {len(cloudtrail.get('active_trails', []))}, Inactive trails: {len(cloudtrail.get('inactive_trails', []))}"
    #     risks.append(risk_msg)
    #     send_alert(
    #         subject="Security Alert: CloudTrail Not Enabled",
    #         message=risk_msg
    #     )
    # login_attempts = findings.get('login_attempts', {})
    # failed_login_count = login_attempts.get('failed_login_count', 0)
    # if failed_login_count > 0:
    #     failed_logins = login_attempts.get('failed_logins', [])
    #     login_summary = "\n".join([
    #         f"  - {login.get('user', 'Unknown')} from {login.get('source_ip', 'Unknown')} at {login.get('time', 'Unknown')}"
    #         for login in failed_logins[:5]
    #     ])
    #     if len(failed_logins) > 5:
    #         login_summary += f"\n  ... and {len(failed_logins) - 5} more"
    #     risk_msg = f"ALERT: {failed_login_count} failed login attempt(s) detected in last 24 hours:\n{login_summary}"
    #     risks.append(risk_msg)
    #     send_alert(
    #         subject="Security Alert: Failed Login Attempts Detected",
    #         message=risk_msg
    #     )
    
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

