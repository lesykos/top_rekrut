"""
Unit tests for API utility helpers.

This module ensures query parameter decoding and range handling works correctly.
"""

import pytest
from app.api.utils import (
    decode_and_validate_query_params,
    resolve_start_end_from_range,
    get_offset_limit_from_range,
)
from app.core.exceptions import BadRequestError


class TestApiUtils:
    @pytest.mark.unit
    def test_decode_sort_filter_range_success(self):
        args = decode_and_validate_query_params(
            sort='["name", "ASC"]',
            range_param="[0, 10]",
            filter_param='{"id": [1, 2, 3]}',
        )

        assert args["sort_value"] == ["name", "ASC"]
        assert args["range_value"] == [0, 10]
        assert args["filter_value"] == {"id": [1, 2, 3]}

    @pytest.mark.unit
    def test_decode_invalid_json_raises_bad_request(self):
        with pytest.raises(BadRequestError):
            decode_and_validate_query_params(
                sort="[invalid]", range_param=None, filter_param=None
            )

    @pytest.mark.unit
    def test_decode_invalid_sort_raises_bad_request(self):
        with pytest.raises(BadRequestError):
            decode_and_validate_query_params(
                sort='["name"]', range_param=None, filter_param=None
            )

    @pytest.mark.unit
    def test_decode_invalid_filter_raises_bad_request(self):
        with pytest.raises(BadRequestError):
            decode_and_validate_query_params(
                sort=None, range_param=None, filter_param="[1,2,3]"
            )

    @pytest.mark.unit
    def test_decode_invalid_filter_id_type_raises_bad_request(self):
        with pytest.raises(BadRequestError):
            decode_and_validate_query_params(
                sort=None, range_param=None, filter_param='{"id": ["1", "2"]}'
            )

    @pytest.mark.unit
    def test_decode_invalid_range_raises_bad_request(self):
        with pytest.raises(BadRequestError):
            decode_and_validate_query_params(
                sort=None, range_param='[0, "one"]', filter_param=None
            )

    @pytest.mark.unit
    def test_resolve_start_end_with_range(self):
        start, end = resolve_start_end_from_range([2, 5], 10)
        assert start == 2
        assert end == 5

    @pytest.mark.unit
    def test_resolve_start_end_clamps_to_bounds(self):
        start, end = resolve_start_end_from_range([100, 200], 5)
        assert start == 4
        assert end == 4

    @pytest.mark.unit
    def test_resolve_start_end_when_none(self):
        start, end = resolve_start_end_from_range(None, 0)
        assert start == 0
        assert end == 0

    @pytest.mark.unit
    def test_get_offset_limit_from_range(self):
        offset, limit = get_offset_limit_from_range([1, 3])
        assert offset == 1
        assert limit == 3

    @pytest.mark.unit
    def test_get_offset_limit_from_range_none(self):
        offset, limit = get_offset_limit_from_range(None)
        assert offset is None
        assert limit is None
