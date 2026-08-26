import json
from pathlib import Path


class ConfigError(Exception):
    """Raised when application configuration is invalid."""
    

class Config:
    """Loads and validates application configuration."""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        # self.timeout = None
        # self.retry_count = None
        # self.retry_delay = None

    def load(self) -> None:
        """Load configuration from the JSON file."""

        if not self.config_path.exists():
            raise ConfigError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with self.config_path.open("r", encoding="utf-8") as file:
                config_data = json.load(file)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"Invalid JSON configuration: {error}"
            ) from error

        self._validate(config_data)

        self.timeout = config_data["timeout"]
        self.retry_count = config_data["retry_count"]
        self.retry_delay = config_data["retry_delay"]

    def _validate(self, config_data: dict) -> None:
        """Validate configuration values."""

        required_fields = [
            "timeout",
            "retry_count",
            "retry_delay"
        ]

        for field in required_fields:
            if field not in config_data:
                raise ConfigError(
                    f"Missing required configuration field: {field}"
                )

        if not isinstance(config_data["timeout"], (int, float)):
            raise ConfigError("timeout must be a number")

        if config_data["timeout"] <= 0:
            raise ConfigError("timeout must be greater than 0")

        if not isinstance(config_data["retry_count"], int):
            raise ConfigError("retry_count must be an integer")

        if config_data["retry_count"] < 0:
            raise ConfigError("retry_count cannot be negative")

        if not isinstance(config_data["retry_delay"], (int, float)):
            raise ConfigError("retry_delay must be a number")

        if config_data["retry_delay"] < 0:
            raise ConfigError("retry_delay cannot be negative")