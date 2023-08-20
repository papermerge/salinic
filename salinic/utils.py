

def get_db_path(dsn: str) -> str:
    return dsn.split('://')[1]


def first(iterable, condition=None):
    """Returns first item in the iterable matching condition

    If there is no condition provided just return first item.
    If there is no matching item or iterable is empty - just return None
    """
    if iterable is None:
        return None

    try:
        if condition is not None:
            return next(item for item in iterable if condition(item))

        return next(item for item in iterable)
    except StopIteration:
        return None


def trim_suffixes(some_dict):
    result = {}
    for key, value in some_dict.items():
        new_key = key.split('_txt_')[0]
        result[new_key] = value

    return result


def filter_keys(some_dict, keys_to_filter):
    return {
        key: value
        for key, value in some_dict.items() if key not in keys_to_filter
    }
