# django-simple-graphql

## TODO

- Support mutations
- Support subscriptions
- An easy default for authentication
- Account for reverse-relations automatically
- Handle django-graphene issue with relations ponting to non-pk fields and ID encoding
- Configurability
  - Custom set of node interfaces (currently relay.Node)
  - Custom relation connection handler (currently DjangoFilterConnectionField)
  - Custom node/query/mutation/subscription builder functions
  - Custom schema member naming
  - Custom search
  - Enable/disable search globally
  - Enable/disable ordering globally
  - Global default ordering options
  - Injection of GraphQL ID property to models, configurable name and/or disable
- Examples
- More lax version pinning
- Test suite against multiple version configurations
- Proper readme
- Proper type definitions
- GraphQL schema docstring generation
- Validation checks when building the schema to prevent blatantly incorrect config
  - For example, a field in search fields that doesn't exist or isn't supported
- Perhaps a way to auto-render the schema for github diffs?
- A way to easily include extra queries for models (e.g. with different filters)
- Require either field exclusions or inclusions to be explicitly defined
- Build a namespace package instead of a normal one (use "simple_graphql" as namespace root)
- Don't be as tightly coupled with graphene
  - e.g. support to https://github.com/strawberry-graphql/strawberry would be nice


## Features

TODO: Improve the documentation

- Enable GraphQL queries for Django models with a decorator
  - By default, includes a `getModelName` and `listModelName` queries
- Adds a `graphql_node_name` field to model classes
- Adds a `graphql_id` property to models, which can be used to retrieve the
  Global ID of a model instance.
