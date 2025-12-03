import pytest

import local_snowflake as ls


def test_send_request_no_auth_error():
    """
    Ensure that calling send_snow_api_request does not result in an auth error (401/403)
    when credentials are present. If credentials are missing, skip to avoid false negatives.
    """
    # Connections now come from connections.toml only; ensure module initialized
    if ls._snowflake_instance.base_url is None:
        pytest.skip("connections.toml missing or invalid; skipping auth-related integration test.")

    # Call an unlikely path to elicit a non-auth response (e.g., 404) rather than 401/403.
    resp = ls.send_snow_api_request(
        method="GET",
        path="/does-not-exist",
        headers={},
        params={},
        body=None,
        request_guid=None,
        timeout=3000,
    )

    status = resp.get("status")
    content = resp.get("content") or ""

    # The key assertion: no auth error statuses
    assert status not in (401, 403), f"Unexpected auth error status {status}: {content}"


