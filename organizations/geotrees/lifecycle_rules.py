"""Custom lifecycle rules"""

from aws_cdk import aws_s3 as s3


def get_lifecycle_rules() -> list[s3.LifecycleRule]:
    """Custom lifecycle rules. See defaults/lifecycle_rules.py for examples."""
    return []
