"""
Main Lambda Function Handler
Orchestrates metric collection, analysis, and alerting
Owner: Nicole (Automation & Alert Engineer)
"""

import json
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from metrics_collector.metrics_collector import collect_security_metrics
from lambda_handler.alert_manager import check_thresholds_and_alert
from utils.aws_helpers import publish_metrics_to_cloudwatch, handle_error, logger


def lambda_handler(event, context):
    """
    MedTech Security Monitoring Lambda Handler
    Purpose: Automated security metric collection and alerting
    
    This function:
    1. Collects security metrics using Alejandro's metrics_collector module
    2. Publishes metrics to CloudWatch for dashboard visualization
    3. Checks thresholds and sends alerts via SNS if violations detected
    4. Returns status and summary
    
    Expected environment variables:
    - SNS_TOPIC_ARN: ARN of SNS topic for alerts
    - REPORTS_BUCKET: S3 bucket name for reports (optional, for future use)
    """
    
    try:
        logger.info("Starting security metrics collection")
        
        # Step 1: Collect security data from Alejandro's metrics_collector
        findings = collect_security_metrics()
        logger.info(f"Collected {len(findings)} metric categories")
        
        # Step 2: Publish metrics to CloudWatch for dashboard
        publish_metrics_to_cloudwatch(findings)
        logger.info("Metrics published to CloudWatch")
        
        # Step 3: Analyze findings and check thresholds, send alerts if needed
        risks = check_thresholds_and_alert(findings)
        if risks:
            logger.warning(f"Detected {len(risks)} security risks")
        else:
            logger.info("No security risks detected")
        
        # Step 4: Return results
        return {
            'statusCode': 200,
            'body': json.dumps({
                'findings_count': len(findings),
                'risks_detected': len(risks) if risks else 0,
                'risks': risks,
                'message': 'Security metrics collected successfully'
            })
        }
    
    except Exception as e:
        handle_error(e, "lambda_handler")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Error collecting security metrics'
            })
        }

