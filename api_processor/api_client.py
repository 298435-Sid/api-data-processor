import logging
import time

import requests


logger = logging.getLogger(__name__)


class APIClient:
    """Client responsible for communicating with REST APIs."""

    def __init__(
        self,
        timeout: float,
        retry_count: int = 0,
        retry_delay: float = 0
    ):
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def get_data(self, url: str):
        """Send a GET request and return the JSON response."""

        total_attempts = self.retry_count + 1

        for attempt in range(1, total_attempts + 1):

            logger.info(
                "Sending GET request to %s (attempt %d/%d)",
                url,
                attempt,
                total_attempts
            )

            try:
                response = requests.get(
                    url,
                    timeout=self.timeout
                )

                response.raise_for_status()

                logger.info(
                    "API request successful: %s",
                    response.status_code
                )

                return response.json()

            except requests.exceptions.HTTPError as error:

                status_code = (
                    error.response.status_code
                    if error.response is not None
                    else None
                )

                # Retry only for temporary server-side errors
                if (
                    status_code is not None
                    and 500 <= status_code < 600
                    and attempt < total_attempts
                ):
                    logger.warning(
                        "HTTP %s received. Retrying in %s seconds.",
                        status_code,
                        self.retry_delay
                    )

                    time.sleep(self.retry_delay)
                    continue

                logger.error(
                    "HTTP error while accessing API: %s",
                    error
                )

                raise RuntimeError(
                    f"HTTP error while accessing API: {error}"
                ) from error

            except requests.exceptions.ConnectionError as error:

                if attempt < total_attempts:
                    logger.warning(
                        "Connection error. Retrying in %s seconds.",
                        self.retry_delay
                    )

                    time.sleep(self.retry_delay)
                    continue

                logger.error(
                    "Connection error while accessing API: %s",
                    error
                )

                raise RuntimeError(
                    f"Connection error while accessing API: {error}"
                ) from error

            except requests.exceptions.Timeout as error:

                if attempt < total_attempts:
                    logger.warning(
                        "Request timeout. Retrying in %s seconds.",
                        self.retry_delay
                    )

                    time.sleep(self.retry_delay)
                    continue

                logger.error(
                    "Timeout while accessing API: %s",
                    error
                )

                raise RuntimeError(
                    f"Timeout while accessing API: {error}"
                ) from error