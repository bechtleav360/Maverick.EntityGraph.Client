# Maverick EntityGraph Client
This is a Python client for the [Maverick EntityGraph](https://github.com/bechtleav360/Maverick.EntityGraph).
## Requirements.

Python 3.7+

## Installation & Usage
### pip install
```sh
pip install git+https://github.com/bechtleav360/entitygraph-client.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/bechtleav360/entitygraph-client.git`)

Then import the package:
```python
import entitygraph
```

## Getting Started
```python
import entitygraph
from entitygraph import Admin, Entity, Query, Application, Transaction
from rdflib import SDO

# Defining the host is optional and defaults to https://entitygraph.azurewebsites.net
entitygraph.connect(api_key="123")

# For application-specific operations, the Application class is essential. 
# In the following code, an application named "MyApp" is being retrieved. 
# Then, an entity with id "f3f34f" is obtained and converted into the n3 format.
n3: str = Application().get_by_label("MyApp").Entity().get_by_id("f3f34f").n3()

# For operations within the default application, the Admin, Entity, and Query classes can be directly invoked.
# In the example below, an entity with id "g93h4g8" is retrieved and its "foaf.name" value is updated to "New Name".
Entity().get_by_id("g93h4g8").set_value(SDO.title, "New Name")
```