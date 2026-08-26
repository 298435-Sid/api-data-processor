class SummaryGenerator:
    """Generate a summary of processed records."""

    def generate(self, total_records, valid_records, invalid_records, processing_time):
        """Create a processing summary."""

        return {
            "total_records": total_records,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "processing_time": round(processing_time, 2)
        }