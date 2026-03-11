"""Runtime configuration and validation for CDK app execution."""

from typing import Annotated

from pydantic import StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict

IAM_ROLE_ARN_REGEX = r"^arn:aws:iam::\d{12}:role\/[\w+=,.@\-\/]+$"
RoleArn = Annotated[str, StringConstraints(pattern=IAM_ROLE_ARN_REGEX)]


class ConfigSettings(BaseSettings):
    """Environment-backed app settings used at synth/deploy time."""

    model_config = SettingsConfigDict(extra="ignore")

    maap_api_role: RoleArn
    maap_api_user_folder_role: RoleArn


CONFIG = ConfigSettings()
