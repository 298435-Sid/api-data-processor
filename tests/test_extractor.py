from api_processor.extractor import DataExtractor


def test_extract_required_fields():
    extractor = DataExtractor()

    record = {
        "id": 1,
        "name": "Arun",
        "email": "arun@example.com",
        "extra_field": "This should not be included"
    }

    result = extractor.extract(record)

    assert result == {
        "id": 1,
        "name": "Arun",
        "email": "arun@example.com"
    }