# mender-deployer-action

The mender-deployer-action is a very lightweight Github action which allows you to create a Mender deployment via Mender basic auth and Mender's RESTful Management API v1.

## Inputs

### `mender-deployment-name`

_Description:_
Name of the deployment.

_Required:_ *true*

### `mender-artifact-name`

_Description:_
Name of the artifact already sat on the mender server.

_Required:_ *true*

### `mender-device-group`

_Description:_
Name of a predefined device group.

_Required:_ *true*

### `mender-deployment-retries`

_Description:_
Number of deployment retries.

_Required:_ *false*

### `mender-auth-username`

_Description:_
Mender server basic auth username.

_Required:_ *true*

### `mender-auth-password`

_Description:_
Mender server basic auth password.

_Required:_ *true*

### `mender-server-url`

_Description:_
Mender server url.

_Required:_ *true*

## Example usage

```yaml
on: [push]

jobs:
  push-mender-deployment:
    runs-on: ubuntu-latest
    name: Mender deployer pipeline
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Create Mender deployment
        uses: Cein-Markey/mender-deployer-action@v0.1.0-alpha
        id: mender-deployer
        with:
          mender-deployment-name: test-deployment
          mender-artifact-name: release-v0.1.0
          mender-device-group: staging
          mender-deployment-retries: 0
          mender-auth-username: username
          mender-auth-password: password
          mender-server-url: https://hosted.mender.io
```