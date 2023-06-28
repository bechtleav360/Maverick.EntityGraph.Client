# Maverick EntityGraph Client
This is a Python client for the [Maverick EntityGraph](https://github.com/bechtleav360/Maverick.EntityGraph).
## Requirements.

Python 3.7+

## Installation & Usage
### pip install
```sh
pip install git+https://github.com/mumi/entitygraph-client.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/mumi/entitygraph-client.git`)

Then import the package:
```python
import entitygraph
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
import entitygraph

# Defining the host is optional and defaults to https://entitygraph.azurewebsites.net
client = entitygraph.Client(api_key="123")

app_api = client.applications_api

api_response = app_api.list_applications()

print(api_response)

```