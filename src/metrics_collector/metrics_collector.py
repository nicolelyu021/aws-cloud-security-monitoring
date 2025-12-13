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
import json
from typing import Dict, List
from datetime import datetime, timedelta

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
iam = boto3.client('iam')
cloudtrail = boto3.client('cloudtrail')
logs = boto3.client('logs')

def check_encryption() -> List:
    """
    Checks for
    - EBS volume encryption
    """

    # Checks for EBS unecrypted volumes
    volumes = ec2.describe_volumes()['Volumes']
    unencrypted_volumes = []

    for v in volumes:
        if not v['Encrypted']:
            unencrypted_volumes.append(v['VolumeId'])
    
    return unencrypted_volumes

def check_exposure() -> Dict[str, any]:
    """
    Checks for
    - Public EC2 IPs
    - Public S3 buckets
    """

    # Public EC2 IPs
    instances = ec2.describe_instances()
    public_IPs = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:  # Fixed: reservation is a dict, need to access 'Instances' key
            if 'PublicIpAddress' in instance and instance.get('PublicIpAddress'):
                instance_id = instance['InstanceId']
                public_IPs.append(instance_id)
    
    # Public S3 buckets
    public_buckets = []
    
    for bucket in s3.list_buckets()['Buckets']:
        acl = s3.get_bucket_acl(Bucket=bucket['Name'])
        for grant in acl['Grants']:
            if 'AllUsers' in str(grant):
                public_buckets.append(bucket['Name'])

    return {
        "public_ec2_IPs": public_IPs,
        "public_s3_buckets": public_buckets
    }

def check_mfa_iam() -> Dict[str, any]:
    """
    Checks for
    - IAM users without MFA
    - Total numbers of users
    """

    # List of users
    users = iam.list_users()['Users']

    # Check amount IAM users
    total_users = len(users)

    # Check MFA
    non_compliant_users = []
    
    for user in users:
        mfa_devices = iam.list_mfa_devices(UserName = user['UserName'])
        if not mfa_devices['MFADevices']:
            non_compliant_users.append(user['UserName'])

    return {
        "total_users": total_users,
        "non_compliant_users": non_compliant_users
    }

def check_security_groups() -> List:
    """
    Checks for
    - Security groups across all VPCs
    - Detect 0.0.0.0/0 rules
    - Lists ports exposed publicly
    """

    sgs = ec2.describe_security_groups()

    risky_groups = []
    for sg in sgs['SecurityGroups']:
        for rule in sg['IpPermissions']:
            if '0.0.0.0/0' in str(rule):
                risky_groups.append({
                    "SecurityGroupId": sg['GroupId'],
                    "SecurityGroupName": sg.get('GroupName', 'Unknown'),
                    "FromPort": rule.get('FromPort'),
                    "ToPort": rule.get('ToPort'),
                    "Protocol": rule.get('IpProtocol')
                })

    return risky_groups

def check_cloudtrail_status() -> Dict[str, any]:
    """
    Checks if CloudTrail logging is enabled
    Returns status of CloudTrail trails
    """
    try:
        trails = cloudtrail.list_trails()
        active_trails = []
        inactive_trails = []
        
        for trail_info in trails.get('Trails', []):
            trail_name = trail_info['Name']
            try:
                trail_status = cloudtrail.get_trail_status(Name=trail_name)
                
                if trail_status.get('IsLogging', False):
                    active_trails.append(trail_name)
                else:
                    inactive_trails.append(trail_name)
            except Exception as e:
                # If we can't get status, assume inactive
                inactive_trails.append(trail_name)
        
        return {
            "cloudtrail_enabled": len(active_trails) > 0,
            "active_trails": active_trails,
            "inactive_trails": inactive_trails,
            "total_trails": len(trails.get('Trails', []))
        }
    except Exception as e:
        # If CloudTrail API fails, return that it's not configured
        return {
            "cloudtrail_enabled": False,
            "error": str(e),
            "active_trails": [],
            "inactive_trails": [],
            "total_trails": 0
        }

def check_login_attempts() -> Dict[str, any]:
    """
    Checks for failed login attempts via CloudTrail
    Uses CloudTrail LookupEvents to find ConsoleLogin failures
    Returns failed login events from the last 24 hours
    """
    failed_logins = []
    
    try:
        # Look for events in the last 24 hours
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=1)
        
        # Look for ConsoleLogin events
        response = cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'ConsoleLogin'
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50  # Limit to avoid too many results
        )
        
        for event in response.get('Events', []):
            try:
                # Parse the CloudTrail event JSON
                event_data = json.loads(event.get('CloudTrailEvent', '{}'))
                
                # Check if login was successful or failed
                # Failed logins typically have responseElements.ConsoleLogin = "Failure"
                response_elements = event_data.get('responseElements', {})
                console_login = response_elements.get('ConsoleLogin', '')
                
                # Also check for error messages that indicate failure
                error_message = event_data.get('errorMessage', '')
                error_code = event_data.get('errorCode', '')
                
                # Consider it a failure if:
                # 1. ConsoleLogin is explicitly "Failure"
                # 2. There's an error message or error code
                # 3. The response indicates unauthorized access
                is_failure = (
                    console_login == 'Failure' or
                    bool(error_message) or
                    bool(error_code) or
                    'Unauthorized' in str(event_data).lower()
                )
                
                if is_failure:
                    failed_logins.append({
                        "time": event.get('EventTime').isoformat() if event.get('EventTime') else None,
                        "user": event_data.get('userIdentity', {}).get('userName', 'Unknown'),
                        "source_ip": event_data.get('sourceIPAddress', 'Unknown'),
                        "error_message": error_message,
                        "error_code": error_code
                    })
            except (json.JSONDecodeError, KeyError) as e:
                # Skip events that can't be parsed
                continue
        
        return {
            "failed_login_count": len(failed_logins),
            "failed_logins": failed_logins,
            "period_hours": 24,
            "note": "Checking last 24 hours of CloudTrail events"
        }
    except Exception as e:
        # If CloudTrail lookup fails, return empty results with error info
        return {
            "failed_login_count": 0,
            "failed_logins": [],
            "period_hours": 24,
            "error": str(e),
            "note": "CloudTrail lookup failed - check IAM permissions and CloudTrail configuration"
        }

def collect_security_metrics() -> Dict[str, any]:
    """
    Collects all security metrics and returns them in a dictionary.
    This is the main function called by lambda_handler.
    
    Currently collects 4 metric categories:
    1. mfa_iam - IAM MFA compliance
    2. encryption - EBS volume encryption
    3. exposure - Public S3 buckets and EC2 IPs
    4. security_groups - Risky security group rules
    
    Note: CloudTrail and login_attempts functions exist but are commented out
    for presentation consistency with demo screenshots showing 4 categories.
    """
    mfa_iam = check_mfa_iam()
    encryption = check_encryption()
    exposure = check_exposure()
    security_groups = check_security_groups()
    
    # CloudTrail and login_attempts are implemented but disabled for presentation
    # Uncomment these lines to enable (will change to 6 categories, 9 metrics):
    # cloudtrail = check_cloudtrail_status()
    # login_attempts = check_login_attempts()

    return {
        "mfa_iam": mfa_iam,
        "encryption": encryption,
        "exposure": exposure,
        "security_groups": security_groups
        # "cloudtrail": cloudtrail,  # Disabled for presentation
        # "login_attempts": login_attempts  # Disabled for presentation
    }
    

# DONE: Alejandro - Add helper functions for your chosen metrics
# These are just examples - implement the ones you choose:
# - check_public_buckets()
# - check_mfa_compliance()
# - check_security_groups()
# - check_cloudtrail_status()
# - check_failed_logins()
# - or any other security metrics you want to track

# print(check_mfa_iam())
# print(check_security_groups())
# print(check_encryption())
