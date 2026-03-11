#!/usr/bin/env python3
"""CDK app entrypoint for organization bucket deployments."""

import os
from pathlib import Path

import aws_cdk as cdk

from runtime_config import CONFIG
from stacks.buckets_stack import BucketStack
from stacks.logs_stack import LogsStack

ROOT_DIR = Path(__file__).resolve().parent


def _organization_names() -> list[str]:
    organizations_dir = ROOT_DIR / "organizations"
    return sorted(
        path.name.lower()
        for path in organizations_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and not path.name.startswith("_")
    )


def _stack_id(org_name: str) -> str:
    cleaned = "".join(ch for ch in org_name.title() if ch.isalnum())
    return f"{cleaned}Bucket"


app = cdk.App()

# Create centralized logging bucket
logs_stack = LogsStack(
    app,
    "LogsBucket",
    logs_bucket_name="nasa-maap-organization-logs",
)

_organization = os.getenv("ORGANIZATION")
organization_names = _organization_names()

if _organization and _organization not in organization_names:
    raise RuntimeError(f"Unknown organization: {_organization}")

# Create organization buckets with logging to centralized logs bucket
for organization in ([_organization] if _organization else organization_names):
    org_stack = BucketStack(
        app,
        _stack_id(organization),
        org_name=organization,
        maap_api_role_arns=[CONFIG.maap_api_role, CONFIG.maap_api_user_folder_role],
        logs_bucket=logs_stack.logs_bucket,
    )
    org_stack.add_dependency(logs_stack)

app.synth()
