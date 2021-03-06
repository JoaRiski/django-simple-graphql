- GlobalIDInput
  - Enforce data type to be string & add a test case for the check
  - Convert from Scalar to a Field
  - Make serialization possible
  - Validate the correct type of an object ID is passed in, preventing passing in IDs of invalid models
  - Automatically query the model instance instead of just returning the ID.
- Auth
  - Allow substitution of token model
  - Allow substitution of authenticator
  - Allow use of multiple authenticators
  - Allow setting authentication requirements on a schema level
  - Improve type hints (remove use of `Any`)
  - Token model Django admin
  - Authorization rules for queries (make it possible to make the GraphQL API require auth)
  - Middleware for disabling introspection
- General
  - Either get rid of the `simple_graphql.django` module entirely or move the
    `simple_graphql.auth` module under it. Currently undoable due to recursive
    imports.
  - Remove the hack used for toggling introspection disabling middleware during
    test runs and replace it with something better.
  - Lazy schema references to avoid circular imports when defining queries & mutations
  - Figure out what is eating error messages occurring during model build
  - Add support for defining field options (e.g. required) when registering queries
  - Add support for defining custom resolver when registering queries
  - Ensure custom queries don't overlap auto-generated queries
  - Add tests ensuring registering conflict checks work
  - Fix applying of default_ordering and add tests ensuring it works as expected
  - Change default_ordering to accept a list as well as a string
