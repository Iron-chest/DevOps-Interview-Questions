# AWS Lambda Notes Application

This project implements an AWS Lambda function for a notebook application. The function performs basic authentication and returns notes for an authenticated user. The function integrates with DynamoDB for data storage and is exposed via API Gateway as an HTTP request handler. The runtime environment for this Lambda function is Python 3.8.

## Project Description

The application supports the following functionalities:

1. **User Authentication:**
   - Authenticates users based on a token passed in the `Authorization` HTTP header in the format `Bearer <TOKEN>`.
   - Maps the token to the user's email address using the `token-email-lookup` DynamoDB table.

2. **Fetching Notes:**
   - Retrieves notes from the `user_notes` DynamoDB table for the authenticated user.
   - Notes are sorted by the `create_date` attribute in descending order.
   - A maximum of 10 notes are returned per query.

3. **Error Handling:**
   - Returns a 403 status code if the token is invalid or empty.
   - Returns a 400 status code if the `Authorization` header is malformed or missing.

## DynamoDB Tables

### `user_notes` Table
- **Attributes:**
  - `id`: UUID v4, unique identifier for each note.
  - `user`: The email address of the note owner.
  - `create_date`: Creation date in ISO 8601 format.
  - `text`: Content of the note.

- **Keys and Indexes:**
  - Partition key: `user`
  - Sort key: `create_date`

### Example Rows:
| user               | create_date           | text          | id                                    |
|--------------------|-----------------------|---------------|---------------------------------------|
| test@example.com   | 2019-01-01T17:42:34Z | Sample note   | 481ee6ce-f810-42eb-acfe-20a96e34a168 |
| john@doe.com       | 2019-01-02T17:42:34Z | Another note  | 26279956-e2ad-4c78-9f7d-a5a5b7820bad |

### `token-email-lookup` Table
- **Attributes:**
  - `token`: Authentication token.
  - `email`: Email address associated with the token.

- **Keys and Indexes:**
  - Partition key: `token`

### Example Rows:
| email              | token                |
|--------------------|----------------------|
| test@example.com   | 25d73ffca742        |
| john@doe.com       | 6579e96f76ba        |

## Prerequisites

### Software Requirements
- Python 3.8
- AWS CLI
- AWS SAM CLI (optional, for local testing)
- boto3 (AWS SDK for Python)
- Access to AWS services (IAM roles/permissions for Lambda and DynamoDB)

### AWS Resources
- Two DynamoDB tables:
  - `user_notes`
  - `token-email-lookup`
- API Gateway setup to expose the Lambda function as an HTTP handler.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd aws-lambda-notes
   ```

2. **Install Dependencies:**
   Install `boto3` for interacting with AWS services:
   ```bash
   pip install boto3
   ```

3. **Set Up AWS CLI:**
   Configure the AWS CLI with your credentials:
   ```bash
   aws configure
   ```

4. **Deploy the DynamoDB Tables:**
   Create the `user_notes` and `token-email-lookup` tables in DynamoDB via the AWS Management Console or CLI.

5. **Deploy the Lambda Function:**
   - Package the Lambda code:
     ```bash
     zip -r lambda_function.zip .
     ```
   - Deploy the function:
     ```bash
     aws lambda create-function \
       --function-name NotesHandler \
       --runtime python3.8 \
       --role <IAM_ROLE_ARN> \
       --handler lambda_function.lambda_handler \
       --zip-file fileb://lambda_function.zip \
       --timeout 10
     ```

6. **Integrate with API Gateway:**
   Create an API Gateway HTTP API to route requests to the Lambda function.

## Usage

### Authentication
The `Authorization` header must include a valid token in the format `Bearer <TOKEN>`.

### API Endpoints
- **GET /notes**: Retrieves notes for the authenticated user.

### Example Request
```bash
curl -X GET https://<api_gateway_url>/notes \
  -H "Authorization: Bearer 25d73ffca742"
```

### Example Response
```json
[
  {
    "id": "481ee6ce-f810-42eb-acfe-20a96e34a168",
    "user": "test@example.com",
    "create_date": "2019-01-01T17:42:34Z",
    "text": "Sample note"
  }
]
```

## Error Responses
- **400:** `Authentication header is malformed or missing.`
- **403:** `Invalid or empty token.`

## Testing Locally
Use AWS SAM CLI or mock the AWS services with tools like `moto`.

1. **Install SAM CLI:**
   ```bash
   brew install aws-sam-cli
   ```

2. **Run Locally:**
   ```bash
   sam local invoke NotesHandler -e events/event.json
   ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## Note
The coding assessment was done in a simulated environment. Therefore the program might not work as expected on your local device.
