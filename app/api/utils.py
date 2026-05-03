import json
from app.core.exceptions import BadRequestError


def decode_and_validate_query_params(sort, range_param, filter_param):
    try:
        sort_value = json.loads(sort) if sort else None
        filter_value = json.loads(filter_param) if filter_param else {}
        range_value = json.loads(range_param) if range_param else None
    except json.JSONDecodeError as exc:
        raise BadRequestError(f"Invalid query JSON: {exc.msg}") from None

    if sort_value is not None:
        if not (
            isinstance(sort_value, list)
            and len(sort_value) == 2
            and all(isinstance(v, str) for v in sort_value)
            and sort_value[1].upper() in {"ASC", "DESC"}
        ):
            raise BadRequestError(
                "Invalid query: sort must be [field, ASC|DESC]."
            ) from None

    if not isinstance(filter_value, dict):
        raise BadRequestError("Invalid query: filter must be an object.") from None

    if "id" in filter_value:
        ids = filter_value["id"]
        if not (isinstance(ids, list) and all(isinstance(v, int) for v in ids)):
            raise BadRequestError(
                "Invalid query: filter.id must be list[int]."
            ) from None

    if range_value is not None:
        if not (
            isinstance(range_value, list)
            and len(range_value) == 2
            and all(isinstance(v, int) for v in range_value)
        ):
            raise BadRequestError("Invalid query: range must be [start:int, end:int].")

    return {
        "sort_value": sort_value,
        "filter_value": filter_value,
        "range_value": range_value,
    }


def resolve_start_end_from_range(
    range_value: list[int] | None, all_counted: int
) -> tuple[int, int]:
    max_index = max(0, all_counted - 1)
    if range_value is not None:
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
