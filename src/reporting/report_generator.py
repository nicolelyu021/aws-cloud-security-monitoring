"""
Report Generator Module
Generates daily/weekly JSON or CSV summary reports
Owner: Kelly (Reporting & Visualization Lead)

IMPLEMENTATION GUIDANCE:
This module generates reports from the metrics collected by Alejandro's metrics_collector.
Use the exact variable names and structure specified below to ensure compatibility with
Nicole's lambda_handler.py and email_sender.py.

IMPORTANT VARIABLE NAMES:
- metrics: Dict[str, any] - The output from collect_security_metrics()
- report: Dict[str, any] - The formatted report dictionary
- bucket_name: str - S3 bucket name (from environment variable REPORTS_BUCKET)
- key: str - S3 object key (format: 'reports/daily/YYYY-MM-DD.json' or 'reports/weekly/YYYY-MM-DD.json')
"""

import json
import csv
from datetime import datetime
from typing import Dict, List


def generate_daily_report(metrics: Dict[str, any]) -> Dict[str, any]:
    """
    Generates daily summary report from CloudWatch metrics or S3 logs.
    
    IMPLEMENTATION NOTES:
    - Input 'metrics' comes from Alejandro's collect_security_metrics() function
    - Must include these exact keys in the report:
      - 'date': ISO format date string
      - 'report_type': 'daily'
      - 'summary': dict with total_metrics_checked and findings
    - The 'findings' key should contain the full metrics dictionary
    
    Args:
        metrics: Dictionary of security metrics from collect_security_metrics()
                 Format: {'public_s3_buckets': [...], 'mfa_compliance': {...}, ...}
        
    Returns:
        Formatted report dictionary with structure:
        {
            'date': 'YYYY-MM-DDTHH:MM:SS',
            'report_type': 'daily',
            'summary': {
                'total_metrics_checked': int,
                'findings': metrics
            }
        }
    """
    # TODO: Kelly - Implement daily report generation
    # Use this exact structure:
    report = {
        'date': datetime.now().isoformat(),
        'report_type': 'daily',
        'summary': {
            'total_metrics_checked': len(metrics),
            'findings': metrics  # Include full metrics dict
        }
    }
    return report


def generate_weekly_report(metrics_list: List[Dict[str, any]]) -> Dict[str, any]:
    """
    Generates weekly aggregated summary report.
    
    IMPLEMENTATION NOTES:
    - Input is a list of daily metrics dictionaries (from 7 days)
    - Aggregate counts across all days
    - Calculate trends (increasing/decreasing violations)
    - Use same structure as daily report but with 'report_type': 'weekly'
    
    Args:
        metrics_list: List of daily metrics dictionaries from generate_daily_report()
                     Each dict has the structure returned by generate_daily_report()
        
    Returns:
        Formatted weekly report dictionary with aggregated data:
        {
            'date': 'YYYY-MM-DDTHH:MM:SS',
            'report_type': 'weekly',
            'summary': {
                'total_metrics_checked': int,
                'aggregated_findings': {...},
                'trends': {...}
            }
        }
    """
    # TODO: Kelly - Implement weekly aggregation logic
    pass


def save_report_to_s3(report: Dict[str, any], bucket_name: str, key: str):
    """
    Saves report to S3 bucket.
    
    IMPLEMENTATION NOTES:
    - Use boto3 s3 client
    - Convert report dict to JSON string
    - Upload to S3 with proper content type: 'application/json'
    - Handle errors gracefully
    
    Args:
        report: Report dictionary from generate_daily_report() or generate_weekly_report()
        bucket_name: S3 bucket name (from environment variable REPORTS_BUCKET)
        key: S3 object key (format: 'reports/daily/YYYY-MM-DD.json' or 'reports/weekly/YYYY-MM-DD.json')
    """
    # TODO: Kelly - Implement S3 upload logic
    # Use boto3.client('s3').put_object()
    # ContentType should be 'application/json'
    pass

