# Change Log

## Unreleased

- Nothing

## 0.5.0

- Added support for custom `get_queryset` function on model GraphQL configs,
  enabling features such as permission based query result filtering and
  select related's.

## 0.4.0

- Added Schema.register_query method for registering queries
- Added Schema.graphql_query decorator for registering queries
- Improved logging of schema building errors

## 0.3.0

- Added GlobalIDInput graphene scalar
- Added Schema.register_mutation method for registering mutations
- Added Schema.graphql_mutation decorator for registering mutations
- Added `simple_graphql.auth` Django app with the following features:
  - GraphQL middleware which can be used to authenticate queries based on the
    HTTP authorization header
  - Token model for maintaining authorized sessions
  - Default login mutation implementation which is easy to take into use
- Added `require_login` model configuration, which will require all queries of
  that model to be authenticated
- Added `DisableIntrospectionMiddleware` which can be used to disallow
  introspection queries

## 0.2.0

- Removed global schema builder instance
- Removed global decorator for model registering to GraphQL schema
- Removed global function for model registering to GraphQL schema
- Added a decorator to schema builder instances which can be used to register
  models to the schema
- Added a function to the schema builder instance which can be used to register
  models to the schema
- Made the `SchemaBuilder.build_schema` return a lazy object instead of building
  the schema immediately, as it can only be built after model imports have
  fully finished
- Added a check ensuring the schema does not get additional entries once it has
  been built
- Simplify schema declaration by allowing the schema object to be used for
  registering models, as opposed to having to use a separate builder
- Added support for basic search
- Added support for ordering

## 0.1.0

- Initial release
- A single global schema instance where models can be registered
- The schema is declared in Relay-style (connections, edges, nodes)
- Enable GraphQL queries for Django models
  - Enabling can be done via a decorator or a function call
  - By default, includes the following queries:
    - `getModelName` for getting a specific instance with an ID
    - `listModelName` for listing model instances
  - Adds a `graphql_node_name` field to model classes
  - Adds a `graphql_id` property to models, which can be used to retrieve the
  Global ID of a model instance.
  - Configure by adding a `GraphQL` meta class to the model class
  - Alternatively supply a configuration class to the decorator
- Also supports model-specific configuration via one of the following:
  - A metaclass on the model class
  - A configuration object passed in the register decorator or function
  - Merge of the two (where paramter takes precedence)
- Supported configuration options
  - `filters`: A `django-filter` compatible set of filters supported on the
    model's QuerySet. List or a Dictionary.
  - `exclude_fields`: A list of field names to exclude from the schema
  - `search_fields`: A list of fields to perform search on
  - `ordering_fields`: A list of fields that can be used to order results
  - `default_ordering`: What ordering to use if none was specified
- `ordering_fields` and `search_fields` don't do anything yet
