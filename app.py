import argparse
import logging

from api_processor.config import Config, ConfigError
from api_processor.processor import DataProcessor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():

    parser = argparse.ArgumentParser(
        description="API Data Processor"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="REST API endpoint URL"
    )

    parser.add_argument(
        "--output",
        default="result.json",
        help="Output JSON file path"
    )

    args = parser.parse_args()

    try:


        config = Config("config.json")
        config.load()

        logger.info(
            "Configuration loaded successfully"
        )

        logger.info(
            "Timeout: %s seconds",
            config.timeout
        )

        logger.info(
            "Retry count: %s",
            config.retry_count
        )

        logger.info(
            "Retry delay: %s seconds",
            config.retry_delay
        )

        processor = DataProcessor(
            api_url=args.url,
            timeout=config.timeout,
            retry_count=config.retry_count,
            retry_delay=config.retry_delay
        )

        summary = processor.process(
            output_file=args.output
        )

        print("\nProcessing Summary")
        print("------------------")

        print(
            f"Total records received : "
            f"{summary['total_records']}"
        )

        print(
            f"Valid records          : "
            f"{summary['valid_records']}"
        )

        print(
            f"Invalid records        : "
            f"{summary['invalid_records']}"
        )

        print(
            f"Processing time        : "
            f"{summary['processing_time']} sec"
        )

    except ConfigError as exc:

        logger.error(
            "Configuration error: %s",
            exc
        )

        print(
            f"\nConfiguration error: {exc}"
        )

    except RuntimeError as exc:

        logger.error(
            "Processing failed: %s",
            exc
        )

        error_message = str(exc).lower()

        if "connection error" in error_message:

            print(
                "\nProcessing failed: Unable to connect to API."
            )

        elif "timeout" in error_message:

            print(
                "\nProcessing failed: API request timed out."
            )

        elif "http error" in error_message:

            print(
                "\nProcessing failed: API returned an HTTP error."
            )

        else:

            print(
                "\nProcessing failed: "
                "An unexpected error occurred."
            )

if __name__ == "__main__":
    main()