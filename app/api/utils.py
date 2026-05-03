def resolve_start_end_from_range(
    range_value: list[int] | None, all_counted: int
) -> tuple[int, int]:
    max_index = max(0, all_counted - 1)
    if range_value:
        start = min(max(0, range_value[0]), max_index)
        end = min(max(range_value[1], start), max_index)
    else:
        start = 0
        end = max_index
    return (start, end)
