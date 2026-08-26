# API Data Processor

## 1. Project Overview

This project is a Python-based API data processing application.

The application:

- Fetches data from a REST API.
- Validates the API response and individual records.
- Extracts the required fields.
- Transforms the data into the required output structure.
- Excludes invalid records from processing.
- Writes the processed records to a JSON file.
- Generates a processing summary.
- Provides a mock REST API for local testing.
- Includes automated tests using pytest.

---

## 2. Processing Flow

```text
Mock REST API
      |
      v
HTTP GET Request
      |
      v
API Client
      |
      v
Response Validation
      |
      v
Record Validation
      |
      +-------------------+
      |                   |
    Valid              Invalid
      |                   |
      v                   v
  Extraction          Excluded
      |
      v
 Transformation
      |
      v
 JSON Writer
      |
      v
 result.json
      |
      v
 Summary Generation
```

---

## 3. Project Structure

The project is organized into separate modules for API communication, validation, extraction, transformation, output generation, and testing.

```text
api-data-processor/
|
|-- app.py
|-- config.json
|-- requirements.txt
|-- README.md
|
|-- api_processor/
|   |
|   |-- __init__.py
|   |-- api_client.py
|   |-- config.py
|   |-- extractor.py
|   |-- json_writer.py
|   |-- processor.py
|   |-- summary.py
|   |-- transformer.py
|   |-- validator.py
|   |
|   `-- mock_api/
|       |
|       |-- __init__.py
|       `-- app.py
|
`-- tests/
    |
    |-- test_api_client.py
    |-- test_config.py
    |-- test_extractor.py
    |-- test_json_writer.py
    |-- test_summary.py
    |-- test_transformer.py
    `-- test_validator.py
```

---

## 4. Configuration

The application configuration is maintained in the `config.json` file.

### Current Configuration

```json
{
    "timeout": 10,
    "retry_count": 3,
    "retry_delay": 0.5
}
```

### Configuration Parameters

- **timeout** : Maximum time allowed for an API response.
- **retry_count** : Number of retry attempts configured.
- **retry_delay** : Delay between retry attempts in seconds.

The configuration is loaded and validated before processing the API data.

---

## 5. Mock API

The project includes a local mock REST API for testing.

### Start Mock API

From the project root:

```bash
python api_processor/mock_api/app.py
```

The mock API runs on:

```text
http://127.0.0.1:8001
```

### Available Endpoints

#### GET /users

Returns test user records.

The current test data contains 500 records, including valid and invalid records.

#### GET /error

Simulates an HTTP 500 Internal Server Error.

#### GET /slow

Simulates a slow API response to test timeout handling.

---

## 6. Running the Application

### Step 1: Start the Mock API

```bash
python api_processor/mock_api/app.py
```

Keep this terminal running.

### Step 2: Open Another Terminal

Navigate to the project root:

```bash
cd api-data-processor
```

Run:

```bash
python app.py
```

The application will:

```text
Fetch API Data
      |
      v
Validate Response
      |
      v
Validate Records
      |
      v
Extract Valid Records
      |
      v
Transform Records
      |
      v
Create result.json
      |
      v
Generate Processing Summary
```

---

## 7. Expected Processing Summary

Example:

```text
Processing Summary
------------------
Total records received : 500
Valid records          : 499
Invalid records        : 1
Processing time        : 0.03 sec
```

The invalid record is not included in the processed output.

---

## 8. Output

The application generates:

### result.json

The output contains the successfully validated and transformed records.

For the current 500-record test:

```text
Total records received : 500
Valid records          : 499
Invalid records        : 1
Processed JSON records : 499
```

---

## 9. Running Tests

Run all tests using:

```bash
python -m pytest -v
```

### Current Test Result

```text
16 passed
```

### Test Coverage

The tests cover:

- API client
- HTTP errors
- Connection failures
- Timeout handling
- Configuration validation
- Response validation
- Record validation
- Data extraction
- Data transformation
- JSON writing
- Summary generation

---

## 10. Error Handling

The API client currently handles the following:

### HTTP Errors

For example:

```text
HTTP 500 Internal Server Error
```

The application raises a `RuntimeError` with an appropriate error message.

### Connection Failures

If the API server cannot be reached, the connection failure is handled gracefully without causing the application to crash unexpectedly.

### Timeout Errors

If the API does not respond within the configured timeout period, the timeout is handled as a `RuntimeError`.

### Invalid Records

Invalid records are detected during validation and excluded from the processed output.

The application continues processing the remaining valid records.

---

## 11. Logging

The application uses Python's built-in `logging` module.

Logging is used for:

- Application events
- Processing information
- Warnings
- Error tracking
- Debugging support

---

## 12. Retry Mechanism

The application supports configurable retries for temporary API failures.

### Retry Settings

Defined in `config.json`:

```json
{
    "timeout": 10,
    "retry_count": 3,
    "retry_delay": 0.5
}
```

---

## 13. Retry Flow

```text
Command Line
     |
     v
    app.py
     |
     v
Load config.json
     |
     +---- timeout
     |
     +---- retry_count
     |
     +---- retry_delay
     |
     v
DataProcessor
     |
     v
APIClient
     |
     v
GET API
     |
     +---- Success ---------> Process 500 Records
     |
     +---- Connection Error
     |          |
     |          v
     |      Retry 3 Times
     |
     +---- Timeout
     |          |
     |          v
     |      Retry 3 Times
     |
     +---- HTTP Error
                |
                v
        Retry / Final Error
```

---

## 14. Technologies Used

- Python
- Requests
- Pytest
- JSON
- HTTP Server
- REST API
- Visual Studio Code (VS Code)

---

## Key Features

- REST API Data Retrieval
- Response Validation
- Record Validation
- Data Extraction
- Data Transformation
- JSON Output Generation
- Processing Summary Reporting
- Mock REST API for Testing
- Retry and Timeout Handling
- Structured Logging
- Automated Testing with Pytest
- Modular Project Architecture