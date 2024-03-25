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

### New entities
An entity object can be newly created using the entity class:
```python
from entitygraph import Entity
# Creates a new entity
new_entity = Entity("application_label")
```

You can only add types to newly created entities:
```python
# Add at least one new type
new_entity.types = "https://schema.org/LearningRecource"
```

Every entity contains values and relations for given predicates.
To add a new value/relation to an entity, access the dictionary-like values/relations property:
```python
# Add at least one new type
new_entity.types = "https://schema.org/LearningRecource"
```

Multiple types/values/relations can be added at once
```python
# Add multiple new types at once
new_entity.types = "https://schema.org/LearningRecource", "https://schema.org/VideoObject"
# or as list
new_entity.types = ["https://schema.org/LearningRecource", "https://schema.org/VideoObject"]

# Add multiple values
new_entity.values["https://schema.org/Keywords"] = "entity graph", "python", "client"
# or as list
new_entity.values["https://schema.org/Keywords"] = ["entity graph", "python", "client"]
```

Add details to a value. Note that only one literal can be added for each detail.
```python
# Access details for a specific value using the "details" method
details = new_entity.values["https://schema.org/Keywords"].details("entity graph")
# Add content in a similar fashion to values
details["https://w3id.org/eav/status"] = "new"
# or in one line
new_entity.values["https://schema.org/Keywords"].details("entity graph")["https://w3id.org/eav/status"] = "new"
```

To remove a value or a detail attached to it
```python
# Remove value
new_entity.values["https://schema.org/Keywords"].remove_content("entity graph")
# Remove all values
new_entity.values["https://schema.org/Keywords"].remove_content(remove_all=True)
# Remove detail
new_entity.values["https://schema.org/Keywords"].details("entity graph")["https://w3id.org/eav/status"].remove_content()
```

RDFlib can be used to access predicates:
```python
from rdflib import SDO

new_entity.values[SDO.keywords] = "entity graph", "python3.7", "client"
```

All in one
```python
from entitygraph import Entity, connect
from rdflib import SDO

connect("vuIZS&JC6KI7pOW47$GZ")

new_entity = Entity("application_label")

new_entity.types = "https://schema.org/LearningRecource", "https://schema.org/VideoObject"

new_entity.values[SDO.name] = "My Entity"
new_entity.values[SDO.keywords] = "entity graph", "python3.7", "client"

new_entity.values[SDO.keywords].details("entity graph")["https://w3id.org/eav/status"] = "new"
new_entity.values[SDO.keywords].details("entity graph")["https://w3id.org/eav/confidence"] = "0"
```

### Existing entities
Existing entities function in the same way as new entities, simply add the id from entity graph
```python
from entitygraph import Entity, connect

connect("vuIZS&JC6KI7pOW47$GZ")

entity = Entity("application_label", id_="entitygraph object id")
```
All other functions are the same. Note that content is always loaded on use only (or when iterating over a container).

### Application class
Entities do not save any changes made, this is what the application class is for.

To save an entity, the "create_entity" and "save_entity" methods are used
```python
from entitygraph import Application, Entity, connect

connect("vuIZS&JC6KI7pOW47$GZ")

entity = Entity("application_label", id_="entitygraph object id")
# Apply changes to entity
...
# Save entity on graph
Application.save_entity(entity)

new_entity = Entity("application_label")
# Apply changes to entity
...
# Create entity on graph
Application.create_entity(new_entity)
```

Entities can be removed using the "delete_entity" or "delete_entity_by_id" methods
```python
from entitygraph import Application, Entity, connect

connect("vuIZS&JC6KI7pOW47$GZ")

entity = Entity("application_label", id_="entitygraph object id")
...
# Delete entity on graph
Application.delete_entity(entity)
# or
Application.delete_entity_by_id("entitygraph object id", "application_label")
```

