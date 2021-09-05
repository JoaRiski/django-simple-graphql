from simple_graphql.django.types import ModelClass


def get_node_name(model_cls: ModelClass) -> str:
    return f"{model_cls.__name__}"
