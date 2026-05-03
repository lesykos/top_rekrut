def resolve_start_end_from_range(
    range_value: list[int] | None, all_counted: int
) -> tuple[int, int]:
    if range_value:
        start = range_value[0]
        end = (
            range_value[1] if range_value[1] < all_counted else max(all_counted - 1, 0)
        )
    else:
        start = 0
        end = max(all_counted - 1, 0)
    return (start, end)
