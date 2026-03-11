"""CDK stack to deploy a centralized logging bucket."""

from typing import Any

from aws_cdk import Stack, Tags, aws_s3 as s3
from constructs import Construct


class LogsStack(Stack):
    """Deploy a centralized logging bucket for S3 access logs."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        logs_bucket_name: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = logs_bucket_name.lower()
        
        self.logs_bucket = s3.Bucket(
            self,
            "LogsBucket",
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
        )
        Tags.of(self.logs_bucket).add("Name", bucket_name)
