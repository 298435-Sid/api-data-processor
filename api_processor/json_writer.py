import json
from pathlib import Path


class JSONWriter:
    """Save processed records to a JSON file."""

    def save(self, records, output_file):
        """Save records to the specified JSON file."""

        output_path = Path(output_file)

        output_data = {
            "processed_records": records
        }

        with output_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                output_data,
                file,
                indent=4
            )