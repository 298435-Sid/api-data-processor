class DataTransformer:
    """Transform validated records into the required output structure."""

    def transform(self, record):
        """Transform a single record."""

        return {
            "user_id": record["id"],
            "name": record["name"],
            "email": record["email"],
            "status": "valid"
        }