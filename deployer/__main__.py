import os
import sys
import requests

from json import dumps as json_dump
from utils import get_logger
from requests.auth import HTTPBasicAuth

DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME', default=None)
ARTIFACT_NAME = os.getenv('ARTIFACT_NAME', default=None)
DEVICE_GROUP = os.getenv('DEVICE_GROUP', default=None)
RETRIES = os.getenv('RETRIES', default=0)

MENDER_AUTH_USERNAME = os.getenv('MENDER_AUTH_USERNAME', default=None)
MENDER_AUTH_PASSWORD = os.getenv('MENDER_AUTH_PASSWORD', default=None)
MENDER_SERVER_URL = os.getenv('MENDER_SERVER_URL', default=None)

def get_jwt() -> str:
    auth_response = requests.post(f'{MENDER_SERVER_URL}/api/management/v1/useradm/auth/login', verify=False, auth=HTTPBasicAuth(MENDER_AUTH_USERNAME, MENDER_AUTH_PASSWORD))
    if auth_response.status_code == 200:
        return auth_response.text
    else:
        raise ValueError('error: Mender credentials invalid.')

def main() -> int:
    logger = get_logger()

    try:
        for env_var in [DEVICE_GROUP, DEPLOYMENT_NAME, ARTIFACT_NAME, MENDER_AUTH_USERNAME, MENDER_AUTH_PASSWORD, MENDER_SERVER_URL]:
            if env_var is None:
                raise ValueError('error: Required environment variables must be set.')

        logger.info('info: Attempting to authenticate against management server...')
        auth_token = get_jwt()
        logger.info('success: Authenticated against Mender management server...')

        logger.info('info: Attempting to deploy artifact to target devices...')
        uploader_response = requests.post(f'{MENDER_SERVER_URL}/api/management/v1/deployments/deployments/group/{DEVICE_GROUP}', 
            data=json_dump({
                "name": DEPLOYMENT_NAME,
                "artifact_name": ARTIFACT_NAME,
                "retries": int(RETRIES)
            }),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            },
            verify=False
        )

        if uploader_response.status_code == 201:
            logger.info('success: Deployment has been successful!')
            return 0
        else:
            raise ValueError(uploader_response.content)
    except Exception as e:
        logger.error(e)
        return 1

if __name__ == '__main__':
    sys.exit(main())