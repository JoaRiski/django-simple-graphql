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
