#!/usr/bin/env python3
"""CDK app entrypoint for organization bucket deployments."""

from pathlib import Path

import aws_cdk as cdk

from runtime_config import CONFIG
from stacks.buckets_stack import BucketStack

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

for organization in _organization_names():
    BucketStack(
        app,
        _stack_id(organization),
        org_name=organization,
        maap_api_role_arns=[CONFIG.maap_api_role, CONFIG.maap_api_user_folder_role],
    )

app.synth()
