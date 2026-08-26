from api_processor.summary import SummaryGenerator


def test_generate_summary():
    generator = SummaryGenerator()

    summary = generator.generate(
        total_records=3,
        valid_records=2,
        invalid_records=1,
        processing_time=2.436
    )

    assert summary == {
        "total_records": 3,
        "valid_records": 2,
        "invalid_records": 1,
        "processing_time": 2.44
    }