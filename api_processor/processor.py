import logging
import time

from api_processor.api_client import APIClient
from api_processor.validator import ResponseValidator
from api_processor.extractor import DataExtractor
from api_processor.transformer import DataTransformer
from api_processor.json_writer import JSONWriter
from api_processor.summary import SummaryGenerator


logger = logging.getLogger(__name__)


class DataProcessor:
    """Coordinate the complete API data processing workflow."""

    def __init__(
        self,
        api_url,
        timeout=10,
        retry_count=0,
        retry_delay=0
    ):
        self.api_url = api_url

        self.client = APIClient(
            timeout=timeout,
            retry_count=retry_count,
            retry_delay=retry_delay
        )

        self.validator = ResponseValidator()
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.json_writer = JSONWriter()
        self.summary_generator = SummaryGenerator()

    def process(self, output_file="result.json"):
        """Fetch and process API records."""

        start_time = time.time()

        logger.info("Starting API data processing")
        logger.info("API URL: %s", self.api_url)
        logger.info("Fetching data from API")

        # 1. Get data from API
        data = self.client.get_data(self.api_url)

        logger.info("Successfully received API response")

        # 2. Validate overall response
        logger.info("Validating API response structure")

        self.validator.validate_response(data)

        total_records = len(data)

        logger.info(
            "Total records received: %d",
            total_records
        )

        valid_records = []
        invalid_records = []

        # 3. Validate and process each record
        for record in data:

            if self.validator.validate_record(record):

                extracted_data = self.extractor.extract(record)

                transformed_data = self.transformer.transform(
                    extracted_data
                )

                valid_records.append(transformed_data)

            else:
                invalid_records.append(record)

                logger.warning(
                    "Invalid record excluded from processing"
                )

        logger.info(
            "Record validation completed: %d valid, %d invalid",
            len(valid_records),
            len(invalid_records)
        )

        # 4. Save valid processed records
        logger.info(
            "Writing %d processed records to %s",
            len(valid_records),
            output_file
        )

        self.json_writer.save(
            valid_records,
            output_file
        )

        logger.info(
            "Processed records successfully written"
        )

        # 5. Calculate processing time
        processing_time = time.time() - start_time

        # 6. Generate summary
        summary = self.summary_generator.generate(
            total_records=total_records,
            valid_records=len(valid_records),
            invalid_records=len(invalid_records),
            processing_time=processing_time
        )

        logger.info(
            "Processing completed: %d total, %d valid, %d invalid",
            total_records,
            len(valid_records),
            len(invalid_records)
        )

        logger.info(
            "Processing time: %.2f seconds",
            processing_time
        )

        return summary