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
This client represents entity graph objects using an Entity object.
Before working with the entity graph, a connection must be established:
```python
from entitygraph import connect

connect("vuIZS&JC6KI7pOW47$GZ")
```

An entity object can either be newly created or already exist:

```python
from entitygraph import Entity, connect

connect("vuIZS&JC6KI7pOW47$GZ")

# Creates a new entity
new_entity = Entity("application_label")

# Creates an existing entity
entity = Entity("application_label", id_="entitygraph object id")
```

If an entity is newly created, it must contain at least one type and one value/relation before saving:
```python
from entitygraph import Entity, connect

connect("vuIZS&JC6KI7pOW47$GZ")

# Creates a new entity
new_entity = Entity("application_label")
# Add a new type
new_entity.types = "https://schema.org/LearningRecource"
```

Every entity contains values and relations for given predicates.
To add a new value/relation to an entity access the dictionary-like values/relations property:

```python
from entitygraph import Entity, connect

connect("vuIZS&JC6KI7pOW47$GZ")

entity = Entity("application_label")

# Add a value using a valid url:
entity.values["https://schema.org/name"] = "Name of your entity"
# Add a value using rdflib's SDO
from rdflib import SDO
entity.values[SDO.text] = "Text of your entity"

# Multiple values for one predicate can be added at the same time:
entity.values[SDO.keywords] = ["entity graph", "python", "client"]

# All values can be accessed using the items method
# This will load all values and their content for an existing entity
print(entity.values.items())
```

Since there is no update logic for literals associated with a predicate, if a value should be replaced,
the old on must be deleted:

```python
from entitygraph import Entity, connect
from rdflib import SDO

connect("vuIZS&JC6KI7pOW47$GZ")

entity = Entity("application_label", id_="entitygraph object id")

# Multiple values for one predicate can be added at the same time:
entity.values[SDO.keywords] = "entity graph", "python3.7", "client"
print(entity.values.items())

# Remove old value...
entity.values[SDO.keywords].remove_content("python3.7")
# ...and add new one
entity.values[SDO.keywords] = "python3.10"
print(entity.values.items())
```