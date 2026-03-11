"""Reusable lifecycle defaults for organization buckets."""

from aws_cdk import Duration, aws_s3 as s3


def default_lifecycle_rules() -> list[s3.LifecycleRule]:
    """Return default lifecycle rules applied to most org buckets."""
    return [
        s3.LifecycleRule(
            enabled=True,
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=Duration.days(30),
                ),
            ],
            abort_incomplete_multipart_upload_after=Duration.days(7),
        )
    ]
