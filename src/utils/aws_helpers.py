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
    
    This function handles common metric types. Adjust based on what Alejandro implements.
    
    Args:
        metrics: Dictionary of metrics to publish from collect_security_metrics()
    """
    try:
        cloudwatch = get_boto3_client('cloudwatch')
        metric_data = []
        
        # Publish public S3 buckets count (from exposure dict)
        exposure = metrics.get('exposure', {})
        public_buckets_count = len(exposure.get('public_s3_buckets', []))
        metric_data.append({
            'MetricName': 'PublicS3Buckets',
            'Value': public_buckets_count,
            'Unit': 'Count'
        })
        
        # Publish public EC2 IPs count (from exposure dict)
        public_ec2_count = len(exposure.get('public_ec2_IPs', []))
        metric_data.append({
            'MetricName': 'PublicEC2Instances',
            'Value': public_ec2_count,
            'Unit': 'Count'
        })
        
        # Publish MFA non-compliance count (from mfa_iam dict)
        mfa_iam = metrics.get('mfa_iam', {})
        non_compliant_count = len(mfa_iam.get('non_compliant_users', []))
        metric_data.append({
            'MetricName': 'MFANonCompliantUsers',
            'Value': non_compliant_count,
            'Unit': 'Count'
        })
        
        # Publish total IAM users count
        total_users = mfa_iam.get('total_users', 0)
        metric_data.append({
            'MetricName': 'TotalIAMUsers',
            'Value': total_users,
            'Unit': 'Count'
        })
        
        # Publish risky security groups count
        risky_sg_count = len(metrics.get('security_groups', []))
        metric_data.append({
            'MetricName': 'RiskySecurityGroups',
            'Value': risky_sg_count,
            'Unit': 'Count'
        })
        
        # Publish unencrypted EBS volumes count
        unencrypted_volumes_count = len(metrics.get('encryption', []))
        metric_data.append({
            'MetricName': 'UnencryptedEBSVolumes',
            'Value': unencrypted_volumes_count,
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

