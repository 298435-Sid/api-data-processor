class ResponseValidator:
    """Validate API response structure and records."""

    REQUIRED_FIELDS = {"id", "name", "email"}

    def validate_response(self, data):
        """Validate the overall API response structure."""

        if not isinstance(data, list):
            raise ValueError("API response must be a list")

        return True

    def validate_record(self, record):
        """Validate an individual record."""

        if not isinstance(record, dict):
            return False

        if not self.REQUIRED_FIELDS.issubset(record.keys()):
            return False

        if not isinstance(record["id"], int):
            return False

        if not isinstance(record["name"], str):
            return False

        if not isinstance(record["email"], str):
            return False

        return True