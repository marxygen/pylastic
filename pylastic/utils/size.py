import sys


def full_size_of(obj) -> int:
    """
    Compute and return full object size (including nested objects)

    :param obj: Object to calculate full size of
    :return: Object size in bytes
    """
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        return (
            size
            + sum(map(full_size_of, obj.keys()))
            + sum(map(full_size_of, obj.values()))
        )
    if isinstance(obj, (list, tuple, set, frozenset)):
        return size + sum(map(full_size_of, obj))
    return size
