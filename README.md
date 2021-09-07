# django-simple-graphql

A stupid simple GraphQL setup for Django

**This project is still a WIP and will receive breaking changes**

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
- More lax version pinning (Min python 3.5 or higher)
- Test suite against multiple version configurations
- Proper readme
- Better type definitions
- GraphQL schema docstring generation
- Validation checks when building the schema to prevent blatantly incorrect config
  - For example, a field in search fields that doesn't exist or isn't supported
- Perhaps a way to auto-render the schema for github diffs?
- A way to easily include extra queries for models (e.g. with different filters)
- Require either field exclusions or inclusions to be explicitly defined
- Build a namespace package instead of a normal one (use "simple_graphql" as namespace root)
- Don't be as tightly coupled with graphene
  - e.g. support to https://github.com/strawberry-graphql/strawberry would be nice
- Automatic CRUD operations
- Support more complex ordering options (as well as explicit naming of ordering)
- Run tests for code included in documentation
- Support for permissions
- Query cost analysis / rate limiting
- Consider supporting an alternative approach where registration decorator
  could be applied to a GraphQL config object instead of the model class
- Allow the register decorator be used with or without function call. Possibly
  also allow it's use as a non-decorator registering function.
- Add support for using the schema builder if there's need to combine with an
  existing graphene schema declaration.


## Features (already supported)

TODO: Improve the documentation

- Enable GraphQL queries for Django models with a decorator
  - By default, includes a `getModelName` and `listModelName` queries
  - Configure by adding a `GraphQL` meta class to the model class
  - Alternatively supply a configuration class to the decorator
- Supported configuration options
  - `filters`: A `django-filter` compatible set of filters supported on the
    model's QuerySet. List or a Dictionary.
  - `exclude_fields`: A list of field names to exclude from the schema
  - `search_fields`: A list of fields to perform search on
  - `ordering_fields`: A list of fields that can be used to order results
  - `default_ordering`: What ordering to use if none was specified
- Adds a `graphql_node_name` field to model classes
- Adds a `graphql_id` property to models, which can be used to retrieve the
  Global ID of a model instance.

## Usage

### Setup

Steps 1-3 are setup for `graphene-django`.
See https://docs.graphene-python.org/projects/django/en/latest/installation/ for
more details.

If you are already using `graphene-django`, you can skip to step 4.

1. Add `graphene-django` to your `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       # ...
       "django.contrib.staticfiles", # Required for GraphiQL
       "graphene_django",
   ]
   ```
2. Add a GraphQL endpoint to the URL config:
   ```python
   from django.urls import path
   from django.views.decorators.csrf import csrf_exempt

   from graphene_django.views import GraphQLView

   urlpatterns = [
       # ...
       path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
   ]
   ```
3. Create a schema file (e.g. `schema.py`) and configure it to Graphene:
   ```python
   # settings.py
   GRAPHENE = {
       "SCHEMA": "myapp.shcema.schema",
   }
   ```
4. Declare the schema in your schema file
   ```python
   # schema.py
   from simple_graphql.django import Schema

   schema = Schema()
   ```


### Default queries

By default, all model classes registered to the schema will get a query for
fetching a single object by ID as well as a list query.

For the sake of an example, let's say we have the following model declaration:

```python
from django.db import models

from myapp.schema import schema

@schema.graphql_model()
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
```

The `graphql_model` decorator will add the model to our GraphQL schema builder,
which will build it into the following schema (relay schema omitted):

```graphql
type Person implements Node {
  id: ID!
  lastName: String!
  firstName: String!
}

type Query {
  getPerson(id: ID!): Person
  listPerson(after: String, before: String, first: Int, last: Int, offset: Int): PersonConnection
}
```

For a more complete example of the generated schema, see
[example/schema.graphql](example/schema.graphql)

### Search

TODO

## Examples

### Registering models

There's two ways models can be added to the schema

#### With a class decorator

```python
from django.db import models

from myapp.schema import schema

@schema.graphql_model()
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
```

#### With a function call

```python
from django.contrib.auth import get_user_model

from myapp.schema import schema

User = get_user_model()

schema.register_model(User)
```

### Configuring models

Model specific schemas can be configured either with a metaclass or passed in
as a parameter. A base configuration also is present regardless of custom
declarations.

If multiple configurations are present, they will be merged in the following
precedence:

1. Configuration supplied via parameters
2. Metaclass based configuration
3. Default configuration

Where lower number means higher priority.

#### Metaclass configuration

```python
from django.db import models

from myapp.schema import schema

@schema.graphql_model()
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    credit_card_number = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.SET_NULL)

    class GraphQL:
        exclude_fields = ["credit_card_number"]
        ordering_fields = ["first_name", "last_name"]
        default_ordering = ["first_name"]
        search_fields = ["first_name", "last_name"]
        filters = ["parent"]
```

#### Parameter configuration (with a class)

```python
from django.db import models

from myapp.schema import schema


class PersonGraphQLConfig:
    exclude_fields = ["credit_card_number"]
    ordering_fields = ["first_name", "last_name"]
    default_ordering = ["first_name"]
    search_fields = ["first_name", "last_name"]
    filters = ["parent"]


@schema.graphql_model(PersonGraphQLConfig)
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    credit_card_number = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.SET_NULL)
```

#### Parameter configuration (with a config object)

```python
from django.db import models

from simple_graphql.django import ModelSchemaConfig

from myapp.schema import schema


@schema.graphql_model(ModelSchemaConfig(
    exclude_fields=["credit_card_number"],
    ordering_fields=["first_name", "last_name"],
    default_ordering=["first_name"],
    search_fields=["first_name", "last_name"],
    filters=["parent"],
))
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    credit_card_number = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.SET_NULL)
```

#### Parameter configuration (function variant)

```python
from django.contrib.auth import get_user_model

from simple_graphql.django import ModelSchemaConfig

from myapp.schema import schema

User = get_user_model()

# Could also use a class here just like with the decorator
schema.register_model(User, ModelSchemaConfig(
    exclude_fields=["password"],
))
```
