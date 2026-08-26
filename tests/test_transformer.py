from api_processor.transformer import DataTransformer


def test_transform_record():
    transformer = DataTransformer()

    record = {
        "id": 1,
        "name": "Arun",
        "email": "arun@example.com"
    }

    result = transformer.transform(record)

    assert result == {
        "user_id": 1,
        "name": "Arun",
        "email": "arun@example.com",
        "status": "valid"
    }