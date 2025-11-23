"""
Shared AWS Helper Functions
Utilities for boto3 client creation, logging, and error handling
Owner: Nicole (Automation & Alert Engineer)
"""

import boto3
import logging
from typing import Dict


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_boto3_client(service_name: str, region: str = 'us-east-1'):
    """
    Creates and returns a boto3 client for the specified service.
    
    Args:
        service_name: AWS service name (e.g., 's3', 'iam', 'cloudwatch')
        region: AWS region
        
    Returns:
        boto3 client instance
    """
    return boto3.client(service_name, region_name=region)


def publish_metrics_to_cloudwatch(metrics: Dict[str, any]):
    """
    Publishes custom metrics to CloudWatch.
    
    IMPORTANT: The 'metrics' dictionary must have these exact keys from Alejandro's metrics_collector:
    - 'public_s3_buckets': List[str]
    - 'mfa_compliance': Dict[str, List[str]]
    - 'security_groups': List[str]
    - 'cloudtrail_status': Dict[str, bool]
    - 'failed_logins': int
    
    Args:
        metrics: Dictionary of metrics to publish from collect_security_metrics()
    """
    try:
        cloudwatch = get_boto3_client('cloudwatch')
        metric_data = []
        
        # Publish public S3 buckets count
        public_buckets_count = len(metrics.get('public_s3_buckets', []))
        metric_data.append({
            'MetricName': 'PublicS3Buckets',
            'Value': public_buckets_count,
            'Unit': 'Count'
        })
        
        # Publish MFA non-compliance count
        mfa_compliance = metrics.get('mfa_compliance', {})
        non_compliant_count = len(mfa_compliance.get('non_compliant', []))
        metric_data.append({
            'MetricName': 'MFANonCompliantUsers',
            'Value': non_compliant_count,
            'Unit': 'Count'
        })
        
        # Publish risky security groups count
        risky_sg_count = len(metrics.get('security_groups', []))
        metric_data.append({
            'MetricName': 'RiskySecurityGroups',
            'Value': risky_sg_count,
            'Unit': 'Count'
        })
        
        # Publish CloudTrail logging status (1 if all logging, 0 if any not logging)
        cloudtrail_status = metrics.get('cloudtrail_status', {})
        all_logging = 1 if cloudtrail_status and all(cloudtrail_status.values()) else 0
        metric_data.append({
            'MetricName': 'CloudTrailAllLogging',
            'Value': all_logging,
            'Unit': 'None'
        })
        
        # Publish failed logins count
        failed_logins = metrics.get('failed_logins', 0)
        metric_data.append({
            'MetricName': 'FailedLoginAttempts',
            'Value': failed_logins,
            'Unit': 'Count'
        })
        
        # Publish all metrics in a single call
        if metric_data:
            cloudwatch.put_metric_data(
                Namespace='MedTech/Security',
                MetricData=metric_data
            )
            logger.info(f"Published {len(metric_data)} metrics to CloudWatch")
    
    except Exception as e:
        handle_error(e, "publish_metrics_to_cloudwatch")


def handle_error(error: Exception, context: str = ""):
    """
    Centralized error handling and logging.
    
    Args:
        error: Exception object
        context: Additional context information
    """
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

