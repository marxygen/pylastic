# pylastic

A user-friendly high-level Elasticsearch client wrapper

# Concept
`ElasticClient` is the class that you'll be working on. It can execute all methods
of `Elasticsearch` class from the official package of the corresponding version but also
provides convenience methods. However, the most useful part is the _indexes_.

## Indexes
You can define an index as a class (although it's technically a dataclass) and define
fields that you would like to have in your index. 

```Python
from typing import Optional
from pylastic.indexes import ElasticIndex


class Comment(ElasticIndex):
    timestamp: int
    author: str
    text: str
    rating: Optional[float]
```

Now the `Comment` class is a dataclass, and you can also do CRUD operations with it. However, we'll
postpone that to review available field definitions.

### Field Definitions
Specify field along with its type using annotations:
```python
string_field: str
integer_field: int
```
You can use Pythonic types, but `pylastic` also provides a `pylastic.types` package with all of the
types ES supports (see them [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)).
These types will be used to *create a mapping* so that ES can correctly process fields in your index.

- `GeoPoint`. Allows to specify fields of type `geo_point`. Supports the following formats:
  - GeoJSON. 
  
    `{ 
      "type": "Point",
      "coordinates": [-71.34, 41.12]
    }`, (lon, lat)
  - WKTP.
  
    `"POINT (-71.34 41.12)"`, (lon, lat)
  - `{ 
    "lat": 41.12,
    "lon": -71.34
  }`
  - `[ -71.34, 41.12 ]`, (lon, lat)
  - `"41.12,-71.34"`, (**lat, lon**)

