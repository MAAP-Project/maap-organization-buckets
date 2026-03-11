"""Reusable S3 bucket policy defaults."""

from aws_cdk import aws_iam as iam, aws_s3 as s3


def apply_default_bucket_policy(
    bucket: s3.IBucket, *, maap_api_role_arns: list[str] | None = None
) -> None:
    """Apply baseline S3 security controls to all managed buckets."""
    statements = [
        iam.PolicyStatement(
            sid="DenyInsecureTransport",
            effect=iam.Effect.DENY,
            actions=["s3:*"],
            principals=[iam.AnyPrincipal()],
            resources=[bucket.bucket_arn, f"{bucket.bucket_arn}/*"],
            conditions={"Bool": {"aws:SecureTransport": "false"}},
        ),
    ]

    if maap_api_role_arns:
        statements.append(
            iam.PolicyStatement(
                sid="MaapApiGetList",
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetBucketLocation",
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:GetObjectTagging",
                    "s3:GetObjectVersionTagging",
                    "s3:ListBucket",
                    "s3:ListBucketMultipartUploads",
                    "s3:ListBucketVersions",
                    "s3:ListMultipartUploadParts",
                ],
                principals=[
                    iam.ArnPrincipal(role_arn) for role_arn in maap_api_role_arns
                ],
                resources=[bucket.bucket_arn, f"{bucket.bucket_arn}/*"],
            )
        )

    apply_policy_statements(bucket, statements)


def apply_policy_statements(
    bucket: s3.IBucket, statements: list[iam.PolicyStatement]
) -> None:
    """Attach one or more resource policy statements to a bucket."""
    for statement in statements:
        bucket.add_to_resource_policy(statement)
