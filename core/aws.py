import boto3
from botocore.config import Config
from botocore.exceptions import EndpointConnectionError, ClientError

from core.config import cred
from core.exceptions import InfraPilotError

DEFAULT_BOTO_CONFIG = Config(
    region_name=cred.AWS_DEFAULT_REGION,
    connect_timeout=5,
    read_timeout=10,
    retries={"max_attempts": 2, "mode": "standard"},
)


def get_aws_client(service_name: str):
    """
    Factory function returning a configured Boto3 client for any AWS service.
    Automatically targets LocalStack if AWS_ENDPOINT_URL is set in .env,
    otherwise falls back to real AWS endpoints.
    """
    client_kwargs = {
        "service_name": service_name,
        "region_name": cred.AWS_DEFAULT_REGION,
        "aws_access_key_id": cred.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": cred.AWS_SECRET_ACCESS_KEY,
        "config": DEFAULT_BOTO_CONFIG,
    }

    if cred.AWS_ENDPOINT_URL:
        client_kwargs["endpoint_url"] = cred.AWS_ENDPOINT_URL

    try:
        return boto3.client(**client_kwargs)
    except Exception as e:
        raise InfraPilotError(f"Failed to initialize AWS client for '{service_name}': {e}")


def check_localstack_health() -> bool:
    """Quick connectivity check against LocalStack S3 API."""
    try:
        s3 = get_aws_client("s3")
        s3.list_buckets()
        return True
    except EndpointConnectionError:
        raise InfraPilotError(
            f"Cannot reach LocalStack at {cred.AWS_ENDPOINT_URL}. Is the container running?"
        )
    except ClientError as e:
        raise InfraPilotError(f"AWS ClientError during health check: {e}")