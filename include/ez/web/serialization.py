from functools import singledispatch


@singledispatch
def serialize(obj):
    raise NotImplementedError(f"Cannot serialize {obj!r}")


serializer = serialize.register


@serializer
def _(obj: dict):
    return {key: serialize(value) for key, value in obj.items()}


@serializer
def _(obj: list):
    return [serialize(item) for item in obj]


@serializer
def _(obj: int):
    return obj


@serializer
def _(obj: bool):
    return obj


@serializer
def _(obj: str):
    return obj
