"""
Report Generator Module
Generates daily/weekly JSON summary reports
Owner: Kelly (Reporting & Visualization Lead)

INTERFACE NOTES:
This module processes metrics from Alejandro's metrics_collector. The input will be
a dictionary with keys: mfa_iam, encryption, exposure, security_groups.

Example structure from collect_security_metrics():

{
    "mfa_iam": {
        "total_users": 10,
        "non_compliant_users": ["alice", "bob"]
    },
    "encryption": ["vol-123", "vol-456"],  # unencrypted volume IDs
    "exposure": {
        "public_ec2_IPs": ["i-abc123", "i-def456"],
        "public_s3_buckets": ["bucket-1", "bucket-2"]
    },
    "security_groups": [
        {
            "SecurityGroupId": "sg-12345",
            "SecurityGroupName": "web-sg",
            "FromPort": 80,
            "ToPort": 80,
            "Protocol": "tcp"
        },
        ...
    ]
}
"""

import json
import boto3
from datetime import datetime
from typing import Dict, List

s3 = boto3.client("s3")

# ------------------------------------------------------------------------------------
# DAILY REPORT
# ------------------------------------------------------------------------------------

def generate_daily_report(metrics: Dict[str, any]) -> Dict[str, any]:
    """
    Generates daily summary report from security metrics returned by collect_security_metrics().
    
    Args:
        metrics: Dictionary from collect_security_metrics() with security findings
        
    Returns:
        Formatted report dictionary
    """

    mfa_iam = metrics.get("mfa_iam", {})
    encryption = metrics.get("encryption", [])
    exposure = metrics.get("exposure", {})
    security_groups = metrics.get("security_groups", [])

    non_compliant_users = mfa_iam.get("non_compliant_users", [])
    total_users = mfa_iam.get("total_users", 0)
    public_ec2 = exposure.get("public_ec2_IPs", [])
    public_buckets = exposure.get("public_s3_buckets", [])

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "period": "daily",
        "summary": {
            "iam": {
                "total_users": total_users,
                "non_compliant_users_count": len(non_compliant_users),
                "non_compliant_users": non_compliant_users,
            },
            "encryption": {
                "unencrypted_volumes_count": len(encryption),
                "unencrypted_volumes": encryption,
            },
            "exposure": {
                "public_ec2_count": len(public_ec2),
                "public_ec2_instances": public_ec2,
                "public_s3_buckets_count": len(public_buckets),
                "public_s3_buckets": public_buckets,
            },
            "security_groups": {
                "risky_sg_count": len(security_groups),
                "risky_sg_details": security_groups,
            },
        },
    }

    return report

# ------------------------------------------------------------------------------------
# WEEKLY REPORT
# ------------------------------------------------------------------------------------

def generate_weekly_report(metrics_list: List[Dict[str, any]]) -> Dict[str, any]:
    """
    Generates weekly aggregated summary report.
    
    Args:
        metrics_list: List of raw metrics dicts (one per day) from collect_security_metrics()
        
    Returns:
        Weekly aggregated report dictionary
    """

    all_non_compliant_users = set()
    all_unencrypted_vols = set()
    all_public_ec2 = set()
    all_public_buckets = set()
    all_risky_sg_ids = set()

    total_users_last_day = 0  # keep last observed total_users as context

    for day in metrics_list:
        mfa_iam = day.get("mfa_iam", {})
        encryption = day.get("encryption", [])
        exposure = day.get("exposure", {})
        security_groups = day.get("security_groups", [])

        # IAM
        total_users_last_day = mfa_iam.get("total_users", total_users_last_day)
        all_non_compliant_users.update(mfa_iam.get("non_compliant_users", []))

        # Encryption
        all_unencrypted_vols.update(encryption)

        # Exposure
        all_public_ec2.update(exposure.get("public_ec2_IPs", []))
        all_public_buckets.update(exposure.get("public_s3_buckets", []))

        # Security groups
        for sg in security_groups:
            sg_id = sg.get("SecurityGroupId")
            if sg_id:
                all_risky_sg_ids.add(sg_id)

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "period": "weekly",
        "summary": {
            "iam": {
                "total_users_last_observed": total_users_last_day,
                "unique_non_compliant_users": list(all_non_compliant_users),
                "unique_non_compliant_users_count": len(all_non_compliant_users),
            },
            "encryption": {
                "unique_unencrypted_volumes": list(all_unencrypted_vols),
                "unique_unencrypted_volumes_count": len(all_unencrypted_vols),
            },
            "exposure": {
                "unique_public_ec2_instances": list(all_public_ec2),
                "unique_public_ec2_count": len(all_public_ec2),
                "unique_public_s3_buckets": list(all_public_buckets),
                "unique_public_s3_buckets_count": len(all_public_buckets),
            },
            "security_groups": {
                "unique_risky_sg_ids": list(all_risky_sg_ids),
                "unique_risky_sg_count": len(all_risky_sg_ids),
            },
        },
    }

    return report


# ------------------------------------------------------------------------------------
# SAVE TO S3
# ------------------------------------------------------------------------------------

def save_report_to_s3(report: Dict[str, any], bucket_name: str, key: str):
    """
    Saves report dictionary to S3 bucket as JSON.
    
    Args:
        report: Report dictionary to save
        bucket_name: S3 bucket name (from environment variable REPORTS_BUCKET)
        key: S3 object key (e.g., 'reports/daily/report_2025-11-27.json')
    """

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(report, indent=2),
            ContentType="application/json"
        )
        print(f"Report saved to s3://{bucket_name}/{key}")

    except Exception as e:
        print("Error uploading report to S3:", e)
        raise

# ------------------------------------------------------------------------------------
# LOCAL TESTING
# ------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Running local test for report_generator.py...\n")

    sample_metrics = {
        "mfa_iam": {
            "total_users": 5,
            "non_compliant_users": ["alice", "bob"]
        },
        "encryption": ["vol-123", "vol-456"],
        "exposure": {
            "public_ec2_IPs": ["i-abc123"],
            "public_s3_buckets": ["bucket-1"]
        },
        "security_groups": [
            {
                "SecurityGroupId": "sg-12345",
                "SecurityGroupName": "web-sg",
                "FromPort": 80,
                "ToPort": 80,
                "Protocol": "tcp"
            }
        ]
    }

    daily = generate_daily_report(sample_metrics)
    print("DAILY REPORT:")
    print(json.dumps(daily, indent=2))

    weekly = generate_weekly_report([sample_metrics] * 7)
    print("\nWEEKLY REPORT:")
    print(json.dumps(weekly, indent=2))
