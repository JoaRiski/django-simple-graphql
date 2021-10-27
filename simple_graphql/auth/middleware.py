from typing import Any

from django.contrib.auth.models import AnonymousUser

from simple_graphql.auth.auth import TokenAuthentication

AUTH = TokenAuthentication()


def auth_middleware(get_response: Any, root: Any, info: Any, **args: Any) -> Any:
    # TODO: Replace Any types with better types
    graphql_authenticated = getattr(info.context, "graphql_authenticated", False)
    if not hasattr(info.context, "user") or (
        info.context.user and not graphql_authenticated
    ):
        info.context.user = AnonymousUser()
    if info.context.META.get("HTTP_AUTHORIZATION") and not graphql_authenticated:
        auth_result = AUTH.authenticate(info.context)
        if auth_result:
            info.context.user = auth_result[0]
            info.context.graphql_authenticated = True
    return get_response(root, info, **args)
