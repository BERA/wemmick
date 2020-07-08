#!/usr/bin/env python
"""
Start webserver after loading environment variables.
"""
import click_spinner


def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the payload for the given secret version if one exists.

    https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#secretmanager-access-secret-version-python
    """
    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient(credentials=9)
    name = client.secret_version_path(project_id, secret_id, version_id)
    response = client.access_secret_version(name)
    payload = str(response.payload.data.decode("UTF-8"))
    return payload


if __name__ == "__main__":
    import os
    import uvicorn
    import google

    # TODO load all secrets needed (deal with gross coupling issues)
    def load_secrets():
        for secret_name in ["GREAT_EXPECTATIONS_SLACK_WEBHOOK"]:
            try:
                print(f"Retrieving secret {secret_name} from Google Secret Manager")
                with click_spinner.spinner():
                    secret = access_secret_version("sdap-dev-k28b8c", secret_name, 1)
            except google.api_core.exceptions.PermissionDenied:
                secret = ""
            # Set environment variables
            # TODO align secret names to prevent mapping
            # os.environ["SLACK_WEBHOOK"] = slack_webhook
            os.environ[secret_name] = secret

    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "127.0.0.1")
    print("running server")
    uvicorn.run("server:app", host=host, port=port, log_level="info")
