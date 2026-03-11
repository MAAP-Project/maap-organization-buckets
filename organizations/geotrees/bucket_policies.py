"""Custom bucket policies"""

from aws_cdk import aws_iam as iam


def get_policy_statements() -> list[iam.PolicyStatement]:
    """Custom bucket policy statements. See defaults/bucket_policies.py for examples."""
    return []
