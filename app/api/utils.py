from app.core.exceptions import BadRequestError


def resolve_start_end_from_range(
    range_value: list[int] | None, all_counted: int
) -> tuple[int, int]:
    max_index = max(0, all_counted - 1)
    if range_value is not None:
        if len(range_value) != 2:
            raise BadRequestError("Invalid query: range must be [start, end].")
        if not all(isinstance(v, int) for v in range_value):
            raise BadRequestError("Invalid query: range values must be integers.")
        start = min(max(0, range_value[0]), max_index)
        end = min(max(start, range_value[1]), max_index)
    else:
        start = 0
        end = max_index
    return (start, end)


def get_offset_limit_from_range(range_: list[int] | None):
    if range_ is not None:
        start, end = resolve_start_end_from_range(range_, pow(9, 9))
        offset = start
        limit = end - start + 1
    else:
        offset = None
        limit = None
    return (offset, limit)
