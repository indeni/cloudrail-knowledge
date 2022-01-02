from enum import EnumMeta


def is_valid_enum_value(enum_meta_class: EnumMeta, value) -> bool:
    return value in set(item.value for item in enum_meta_class)


def enum_implementation(enum_meta_class, value, default=None):
    return enum_meta_class(value) if is_valid_enum_value(enum_meta_class, value) else default
