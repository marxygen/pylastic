

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

