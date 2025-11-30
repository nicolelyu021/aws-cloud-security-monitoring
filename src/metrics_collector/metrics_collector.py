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

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
iam = boto3.client('iam')

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
        for instance in reservation:
            if 'PublicIpAddress' in instance:
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

def check_login_attempts():
    pass

def collect_security_metrics() -> Dict[str, any]:
    mfa_iam = check_mfa_iam()
    encryption = check_encryption()
    exposure = check_exposure()
    security_groups = check_security_groups()

    return {
        "mfa_iam": mfa_iam,
        "encryption": encryption,
        "exposure": exposure,
        "security_groups": security_groups
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
