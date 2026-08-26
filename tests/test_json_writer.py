import json

from api_processor.json_writer import JSONWriter


def test_save_json(tmp_path):
    writer = JSONWriter()

    records = [
        {
            "user_id": 1,
            "name": "Arun",
            "email": "arun@example.com",
            "status": "valid"
        }
    ]

    output_file = tmp_path / "result.json"

    writer.save(records, output_file)

    assert output_file.exists()

    with output_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    assert data["processed_records"] == records