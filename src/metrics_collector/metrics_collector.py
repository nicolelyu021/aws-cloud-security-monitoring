"""
Metrics Collector Module
Collects 3-5 security metrics via boto3
Owner: Alejandro (Infrastructure & Metrics Architect)

INTERFACE CONTRACT (for integration with lambda_handler):
Please return a dictionary from collect_security_metrics() so Nicole's code can process it.
You choose which 3-5 metrics to implement - just make sure the return format is consistent.

Feel free to reach out if you want to discuss the interface or have suggestions!
"""

import boto3
from typing import Dict, List


def collect_security_metrics() -> Dict[str, any]:
    """
    Collects security metrics from AWS services.
    
    Choose 3-5 security metrics to track (e.g., public S3 buckets, MFA compliance,
    security groups, CloudTrail status, failed logins, etc.)
    
    Returns:
        Dictionary with your chosen metric keys and their values
    """
    # TODO: Alejandro - Implement metric collection
    # Return a dictionary with your chosen metrics
    pass


# TODO: Alejandro - Add helper functions for your chosen metrics
# These are just examples - implement the ones you choose:
# - check_public_buckets()
# - check_mfa_compliance()
# - check_security_groups()
# - check_cloudtrail_status()
# - check_failed_logins()
# - or any other security metrics you want to track

