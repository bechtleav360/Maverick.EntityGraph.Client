# Maverick EntityGraph Client
This is a Python client for the [Maverick EntityGraph](https://github.com/bechtleav360/Maverick.EntityGraph).
## Requirements.

Python 3.10+

## Installation & Usage
Activate your virtual environment and run either

*for bleeding edge*
```sh
pip install git+https://github.com/bechtleav360/entitygraph-client.git

pip install --upgrade --force git+https://github.com/bechtleav360/entitygraph-client.git 
```
(you may need to run `pip` with root permission)

*for current snapshot release*


```sh
pip install --extra-index-url https://test.pypi.org/simple/ entitygraph-client
```

*for current stable release*
```sh
pip install entitygraph-client
```

Then import the package:
```python
import entitygraph
```


## Getting Started
```python
import entitygraph as meg
from rdflib import SDO


# Defining the host is optional and defaults to https://entitygraph.azurewebsites.net
meg.connect(api_key="...", host="...")

# Fetch an entity from the graph
author: meg.Entity = meg.Entity().get_by_id("...")

# Create a new entity
builder: meg.EntityBuilder = self.app.EntityBuilder(types=SDO.CreativeWork)
builder.addValue(SDO.title, "My new publication")
builder.addRelation(SDO.author, author)
article: meg.Entity = builder.build()

## Commit entity to graph
article.save()

# For application-specific operations, the Application class is essential. 
# In the following code, an application named "MyApp" is being retrieved. 
# Then, an entity with id "f3f34f" is obtained and converted into the n3 format.
n3: str = meg.Application().get_by_label("MyApp").Entity().get_by_id("f3f34f").n3()

# For operations within the default application, the Admin, Entity, and Query classes can be directly invoked.
# In the example below, an entity with id "g93h4g8" is retrieved and its "foaf.name" value is updated to "New Name".
Entity().get_by_id("g93h4g8").set_value(SDO.title, "New Name")
```
