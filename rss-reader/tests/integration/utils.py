"""
Module with test utils.
"""

from typing import Any


def assert_obj_payload(*, payload: dict, exp_payload: dict):
    """Assert object payload matches expected one.

    Args:
        payload (dict): A response payload.
        exp_payload (dict): An expected response payload.

    Raises:
        AssertionError: if payload does not match the expected one.
    """
    assert "id" in payload
    for key, value in exp_payload.items():
        assert exp_payload[key] == value


def assert_err_detail(*, payload: dict, exp_detail: Any):
    """Assert error detail in response payload.

    Args:
        payload (dict): A response payload.
        exp_detail (Any): An expected error detail.

    Raises:
        AssertionError: if error detail in response payload does not match
            the expected one.
    """
    assert payload["detail"] == exp_detail
