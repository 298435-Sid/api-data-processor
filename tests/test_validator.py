import pytest

from api_processor.validator import ResponseValidator


def test_valid_response():
    validator = ResponseValidator()

    data = [
        {
            "id": 1,
            "name": "Arun",
            "email": "arun@example.com"
        }
    ]

    assert validator.validate_response(data) is True


def test_invalid_response_structure():
    validator = ResponseValidator()

    data = {
        "id": 1,
        "name": "Arun",
        "email": "arun@example.com"
    }

    with pytest.raises(
        ValueError,
        match="API response must be a list"
    ):
        validator.validate_response(data)


def test_valid_record():
    validator = ResponseValidator()

    record = {
        "id": 1,
        "name": "Arun",
        "email": "arun@example.com"
    }

    assert validator.validate_record(record) is True


def test_record_missing_field():
    validator = ResponseValidator()

    record = {
        "id": 1,
        "name": "Arun"
    }

    assert validator.validate_record(record) is False


def test_record_invalid_id():
    validator = ResponseValidator()

    record = {
        "id": "abc",
        "name": "Arun",
        "email": "arun@example.com"
    }

    assert validator.validate_record(record) is False