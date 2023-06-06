from collections import defaultdict
from typing import List, Dict, Sequence, Any

from pylastic.utils.size import full_size_of


def is_iterable(obj) -> bool:
    """
    Check if an object is iterable
    NOTE: considers strings and dicts non-iterable objects!

    :param obj:
    :return:
    """
    try:
        if isinstance(obj, (str, dict)):
            return False

        _ = [i for i in obj]
        return True
    except TypeError:
        return False


def group_by_index(entries: List["ElasticIndex"]) -> Dict[str, List["ElasticIndex"]]:
    indexes = defaultdict(list)
    for entry in entries:
        indexes[entry.get_index()].append(entry)
    return indexes


def get_batches_with_size(
    objects: Sequence[Any], max_size_bytes: int
) -> List[List[Any]]:
    """
    Batch objects so that the size of an individual batch does not exceed `max_size_bytes`

    :param objects: Objects to batch
    :param max_size_bytes: Max batch size in bytes
    :return: List of batches
    """
    batches = []

    current_batch = []
    for o in objects:
        if full_size_of(o) + full_size_of(current_batch) >= max_size_bytes:
            batches.append(current_batch)
            current_batch = [o]
        else:
            current_batch.append(o)
    if current_batch:
        batches.append(current_batch)
    return batches
