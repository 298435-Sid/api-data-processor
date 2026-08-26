import pytest

from api_processor.config import Config, ConfigError


def test_valid_configuration(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "timeout": 10,
            "retry_count": 3,
            "retry_delay": 2
        }
        """,
        encoding="utf-8"
    )

    config = Config(str(config_file))
    config.load()

    assert config.timeout == 10
    assert config.retry_count == 3
    assert config.retry_delay == 2


def test_missing_configuration_file():
    config = Config("missing_config.json")

    with pytest.raises(ConfigError):
        config.load()


def test_invalid_timeout(tmp_path):
    config_file = tmp_path / "config.json"

    config_file.write_text(
        """
        {
            "timeout": -1,
            "retry_count": 3,
            "retry_delay": 2
        }
        """,
        encoding="utf-8"
    )

    config = Config(str(config_file))

    with pytest.raises(ConfigError):
        config.load()