"""
Metrics Collector Module
Collects 3-5 security metrics via boto3
Owner: Alejandro (Infrastructure & Metrics Architect)

IMPLEMENTATION GUIDANCE:
This module should collect the following security metrics and return them in a
standardized dictionary format. Use the exact variable names specified below to
ensure compatibility with Nicole's lambda_handler.py and alert_manager.py.

REQUIRED METRICS (choose 3-5):
1. public_s3_buckets: List[str] - Names of S3 buckets with public access
2. mfa_compliance: Dict[str, List[str]] - Format: {'compliant': [...], 'non_compliant': [...]}
3. security_groups: List[str] - Security group IDs with risky rules (0.0.0.0/0)
4. cloudtrail_status: Dict[str, bool] - Format: {'trail_name': is_logging_enabled}
5. failed_logins: int - Count of failed login attempts (from CloudTrail logs)

RETURN FORMAT:
The collect_security_metrics() function MUST return a dictionary with these exact keys:
{
    'public_s3_buckets': List[str],
    'mfa_compliance': Dict[str, List[str]],
    'security_groups': List[str],
    'cloudtrail_status': Dict[str, bool],
    'failed_logins': int
}

If a metric is not implemented, return an empty list/dict/0 as appropriate.
"""

import boto3
from typing import Dict, List


def collect_security_metrics() -> Dict[str, any]:
    """
    Collects security metrics from AWS services.
    
    IMPLEMENTATION NOTES:
    - Use boto3 clients: s3, iam, ec2, cloudtrail, cloudwatch
    - Handle exceptions gracefully (return empty values on error)
    - Use the exact return dictionary structure shown above
    
    Returns:
        Dictionary containing all collected metrics with exact keys:
        - public_s3_buckets: List[str]
        - mfa_compliance: Dict[str, List[str]] with 'compliant' and 'non_compliant' keys
        - security_groups: List[str]
        - cloudtrail_status: Dict[str, bool]
        - failed_logins: int
    """
    # TODO: Alejandro - Implement metric collection
    # Return structure must match exactly:
    metrics = {
        'public_s3_buckets': [],  # List of bucket names
        'mfa_compliance': {'compliant': [], 'non_compliant': []},  # Dict with two lists
        'security_groups': [],  # List of security group IDs
        'cloudtrail_status': {},  # Dict of trail_name: bool
        'failed_logins': 0  # Integer count
    }
    return metrics


def check_public_buckets() -> List[str]:
    """
    Check for publicly accessible S3 buckets.
    
    IMPLEMENTATION NOTES:
    - Use s3.list_buckets() to get all buckets
    - Check bucket ACL or public access block settings
    - Return list of bucket names (strings) that are publicly accessible
    
    Returns:
        List of bucket names (strings) with public access
    """
    pass


def check_mfa_compliance() -> Dict[str, List[str]]:
    """
    Check IAM users for MFA compliance.
    
    IMPLEMENTATION NOTES:
    - Use iam.list_users() to get all users
    - Use iam.list_mfa_devices(UserName=...) for each user
    - Return dict with 'compliant' and 'non_compliant' keys, each containing list of usernames
    
    Returns:
        Dictionary with format: {'compliant': [usernames], 'non_compliant': [usernames]}
    """
    pass


def check_security_groups() -> List[str]:
    """
    Check security groups for risky rules (e.g., 0.0.0.0/0).
    
    IMPLEMENTATION NOTES:
    - Use ec2.describe_security_groups()
    - Check IpPermissions for 0.0.0.0/0 in CidrIp or CidrIpv6
    - Return list of security group IDs (strings)
    
    Returns:
        List of security group IDs (strings) with risky rules
    """
    pass


def check_cloudtrail_status() -> Dict[str, bool]:
    """
    Check CloudTrail logging status.
    
    IMPLEMENTATION NOTES:
    - Use cloudtrail.describe_trails()
    - Check IsLogging status for each trail
    - Return dict with trail name as key and logging status (bool) as value
    
    Returns:
        Dictionary with format: {'trail_name': is_logging_enabled}
    """
    pass


def check_failed_logins() -> int:
    """
    Check for failed login attempts.
    
    IMPLEMENTATION NOTES:
    - Query CloudTrail logs or CloudWatch Logs Insights
    - Look for events like 'ConsoleLogin' with 'Failure' response
    - Count occurrences in last 24 hours
    - Return integer count
    
    Returns:
        Integer count of failed login attempts
    """
    pass

