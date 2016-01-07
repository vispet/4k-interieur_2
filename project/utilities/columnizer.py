"""
The column calculator
"""

import math


def _get_minimum_columns(max_num_columns):
    """
    Calculate pattern deviation
    """
    return int(math.ceil(max_num_columns / 2.0))


def _can_apply_pattern(pattern, item_count):
    """
    Return true if pattern match, false otherwise
    """
    pattern_idx = 0
    while(item_count > 0):
        item_count -= pattern[pattern_idx]
        pattern_idx += 1
        if pattern_idx >= len(pattern):
            pattern_idx = 0

    return True if item_count == 0 else False


def _generate_variations(seed):
    """
    Generate variations recursively
    """
    for item in seed:
        subset = seed[:]
        subset.remove(item)
        for variation in _generate_variations(subset):
            yield (item,) + variation
        yield (item,)


def get_best_pattern(column_space, item_count):
    """
    Generate possible patterns (favorable patterns first)
    """
    maximum = column_space
    minimum = _get_minimum_columns(column_space)

    for pattern in _generate_variations(range(maximum, minimum - 1, -1)):
        if _can_apply_pattern(pattern, item_count):
            return pattern

    # More aggresively
    for pattern in _generate_variations(range(maximum, minimum - 2, -1)):
        if _can_apply_pattern(pattern, item_count):
            return pattern

    # Return fallback
    return (1,)


def get_patterns(max_num_columns_list, num_items):
    """
    Calculate multiple Patterns
    """
    for max_num_columns in max_num_columns_list:
        yield (max_num_columns, get_best_pattern(max_num_columns, num_items))
