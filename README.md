mongorest
=========

This is just a toy module for creating a REST interface to MongoDB which uses `jsonschema`
to validate data before trying to save into MongoDB collection.

## Example

This example creates a REST server with the following routes:
* `GET` `/users/<string:id>` - return a single document from `users` as JSON or `204`
* `PUT` `/users/<string:id>` - `PUT` a JSON document into `users` or `400` if data does not validate with the schema
* `GET` `/users` - get all documents from `users` as JSON

```python
from mongorest import Server

app = Server('test', host='my.db.server', port=27017)

users_schema = {'type': 'object',
                'properties': {
				  'name': {'type': 'string'},
				  'age': {'type': 'number',
				          'minimum': 0},
				  'admin': {'type': 'boolean'}},
				'required': ['name', 'age', 'admin']}
app.register_collection('users', users_schema)
app.run()
```
