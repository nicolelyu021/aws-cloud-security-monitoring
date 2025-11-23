"""
Metrics Collector Module
Collects 3-5 security metrics via boto3
Owner: Alejandro (Infrastructure & Metrics Architect)

INTERFACE CONTRACT (for integration with lambda_handler):
To ensure smooth integration, please return a dictionary with these keys so Nicole's
code can process the metrics. You can choose which metrics to implement (3-5 total).

Expected return format:
{
    'public_s3_buckets': List[str],  # Bucket names with public access
    'mfa_compliance': Dict[str, List[str]],  # {'compliant': [...], 'non_compliant': [...]}
    'security_groups': List[str],  # Security group IDs with risky rules
    'cloudtrail_status': Dict[str, bool],  # {'trail_name': is_logging_enabled}
    'failed_logins': int  # Count of failed login attempts
}

If a metric isn't implemented, return empty list/dict/0. Feel free to reach out if you
want to discuss the interface or have suggestions!
"""

import boto3
from typing import Dict, List


def collect_security_metrics() -> Dict[str, any]:
    """
    Collects security metrics from AWS services.
    
    Returns:
        Dictionary with keys: public_s3_buckets, mfa_compliance, security_groups,
        cloudtrail_status, failed_logins. See module docstring for format details.
    """
    # TODO: Alejandro - Implement metric collection
    # Placeholder return structure for reference:
    metrics = {
        'public_s3_buckets': [],
        'mfa_compliance': {'compliant': [], 'non_compliant': []},
        'security_groups': [],
        'cloudtrail_status': {},
        'failed_logins': 0
    }
    return metrics


def check_public_buckets() -> List[str]:
    """
    Check for publicly accessible S3 buckets.
    
    Returns:
        List of bucket names (strings) with public access
    """
    pass


def check_mfa_compliance() -> Dict[str, List[str]]:
    """
    Check IAM users for MFA compliance.
    
    Returns:
        Dictionary with format: {'compliant': [usernames], 'non_compliant': [usernames]}
    """
    pass


def check_security_groups() -> List[str]:
    """
    Check security groups for risky rules (e.g., 0.0.0.0/0).
    
    Returns:
        List of security group IDs (strings) with risky rules
    """
    pass


def check_cloudtrail_status() -> Dict[str, bool]:
    """
    Check CloudTrail logging status.
    
    Returns:
        Dictionary with format: {'trail_name': is_logging_enabled}
    """
    pass


def check_failed_logins() -> int:
    """
    Check for failed login attempts.
    
    Returns:
        Integer count of failed login attempts
    """
    pass

