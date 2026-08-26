class DataExtractor:
    """Extract required information from validated API records."""

    def extract(self, record):
        """Extract required fields from a record."""

        return {
            "id": record["id"],
            "name": record["name"],
            "email": record["email"]
        }