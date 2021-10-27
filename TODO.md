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
  - Easy to import default mutation for signing in
- General
  - Either get rid of the `simple_graphql.django` module entirely or move the
    `simple_graphql.auth` module under it. Currently undoable due to recursive
    imports.
