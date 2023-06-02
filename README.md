# pylastic

A user-friendly high-level Elasticsearch client wrapper

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

### Defining Fields
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

#### Marking fields as optional
To mark a field as optional, use `typing.Optional` with the type it's supposed to have, e.g. `Optional[GeoPoint]`

#### Creating new field types
1. Subclass `pylastic.types.base.ElasticType`
2. Define `get_valid_object` _class method_ that validates the object definition (see "GeoType" for example)
3. (Optional) Define `Meta.type` that contains ES type name (e.g. `geo_point` for `GeoPoint`, ...)

### Specifying index metadata
Index metadata defines how an `ElasticIndex` subclass is presented in Elasticsearch. The following
fields are available in the `ElasticIndex.Meta` class:
- `index`. Specify a constant index name.
- `index_prefix`. Index prefix to use, **if `is_datastream` is True** 
- `is_datastream`. If `True`, [datastream logic](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html)
will be applied:
  - Index template will be created: `Meta.index_prefix-*`
  - **NOT IMPLEMENTED YET**
- `id_field`. Use one of the fields as `_id` in ES. When deserialized, it'll be replaced with the field name you specify. Defaults to `_id`.
Note that ID field cannot be used in aggregations and is limited to 512 bytes.
To customize index creation, redefine `ElasticIndex.get_index()` method that returns index name.


## Client
`ElasticClient` is the wrapper for the official `Elasticsearch` package and exposes all the available methods but
also provides convenience methods:
- `create(index: ElasticIndex | str, mapping: Optional[dict])`. Creates an index with the mapping