import pytest
from unittest.mock import patch, MagicMock

from requests.exceptions import ConnectionError, Timeout

from api_processor.api_client import APIClient


def test_get_data_from_mock_api():
    client = APIClient(timeout=10)

    data = client.get_data(
        "http://127.0.0.1:8001/users"
    )

    assert isinstance(data, list)
    assert len(data) == 500

    assert data[0]["id"] == 1
    assert data[0]["name"] == "Arun"
    assert data[0]["email"] == "arun@example.com"


def test_http_error():
    client = APIClient(timeout=10)

    with pytest.raises(RuntimeError, match="HTTP error"):
        client.get_data(
            "http://127.0.0.1:8001/error"
        )


def test_connection_error():
    client = APIClient(timeout=10)

    with pytest.raises(RuntimeError, match="Connection error"):
        client.get_data(
            "http://127.0.0.1:8999/users"
        )


def test_timeout_error():
    client = APIClient(timeout=1)

    with pytest.raises(RuntimeError, match="Timeout"):
        client.get_data(
            "http://127.0.0.1:8001/slow"
        )


# ---------------------------------------------------------
# Retry Tests
# ---------------------------------------------------------

def test_retry_on_connection_error():
    client = APIClient(
        timeout=10,
        retry_count=3,
        retry_delay=0
    )

    with patch(
        "api_processor.api_client.requests.get"
    ) as mock_get:

        mock_get.side_effect = ConnectionError(
            "Connection failed"
        )

        with pytest.raises(
            RuntimeError,
            match="Connection error"
        ):
            client.get_data(
                "http://test-api/users"
            )

        # Initial request + 3 retries = 4 attempts
        assert mock_get.call_count == 4


def test_retry_on_timeout():
    client = APIClient(
        timeout=10,
        retry_count=3,
        retry_delay=0
    )

    with patch(
        "api_processor.api_client.requests.get"
    ) as mock_get:

        mock_get.side_effect = Timeout(
            "Request timed out"
        )

        with pytest.raises(
            RuntimeError,
            match="Timeout"
        ):
            client.get_data(
                "http://test-api/users"
            )

        # Initial request + 3 retries = 4 attempts
        assert mock_get.call_count == 4


def test_retry_succeeds_after_temporary_failure():
    client = APIClient(
        timeout=10,
        retry_count=3,
        retry_delay=0
    )

    successful_response = MagicMock()

    successful_response.status_code = 200

    successful_response.json.return_value = [
        {
            "id": 1,
            "name": "Arun",
            "email": "arun@example.com"
        }
    ]

    with patch(
        "api_processor.api_client.requests.get"
    ) as mock_get:

        mock_get.side_effect = [
            ConnectionError("Temporary failure"),
            ConnectionError("Temporary failure"),
            successful_response
        ]

        data = client.get_data(
            "http://test-api/users"
        )

        assert isinstance(data, list)
        assert data[0]["id"] == 1
        assert data[0]["name"] == "Arun"
        assert data[0]["email"] == "arun@example.com"

        # Two failed attempts + one successful attempt
        assert mock_get.call_count == 3