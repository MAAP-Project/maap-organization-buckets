"""CDK stack to deploy a S3 bucket per organization."""

from importlib import import_module
from typing import Any

from aws_cdk import Stack, Tags, aws_s3 as s3
from constructs import Construct

from defaults.bucket_policies import (
    apply_default_bucket_policy,
    apply_policy_statements,
)
from defaults.lifecycle_rules import default_lifecycle_rules


class BucketStack(Stack):
    """Deploy a bucket for a single organization."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        org_name: str,
        maap_api_role_arns: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = f"nasa-maap-{org_name}".lower()
        lifecycle_rules = default_lifecycle_rules() + self._custom_lifecycle_rules(
            org_name
        )

        bucket = s3.Bucket(
            self,
            f"{org_name.title()}Bucket",
            bucket_name=bucket_name,
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            lifecycle_rules=lifecycle_rules,
        )
        Tags.of(bucket).add("Name", bucket_name)

        apply_default_bucket_policy(
            bucket,
            maap_api_role_arns=maap_api_role_arns,
        )
        apply_policy_statements(bucket, self._custom_policy_statements(org_name))

    @staticmethod
    def _custom_policy_statements(org_name: str) -> list:
        """Load optional custom org policy statements."""
        module_name = f"organizations.{org_name}.bucket_policies"
        try:
            module = import_module(module_name)
        except ModuleNotFoundError as exc:
            if exc.name == module_name:
                return []
            raise

        return list(getattr(module, "get_policy_statements", lambda: [])())

    @staticmethod
    def _custom_lifecycle_rules(org_name: str) -> list[s3.LifecycleRule]:
        """Load optional custom org lifecycle rules."""
        module_name = f"organizations.{org_name}.lifecycle_rules"
        try:
            module = import_module(module_name)
        except ModuleNotFoundError as exc:
            if exc.name == module_name:
                return []
            raise

        return list(getattr(module, "get_lifecycle_rules", lambda: [])())
