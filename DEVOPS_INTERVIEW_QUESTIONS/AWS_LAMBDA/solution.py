import json
import boto3
from boto3.dynamodb.conditions import Key


class InvalidResponse(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


# Don't modify this function name and arguments
def query_user_notes(user_email):
    dynamo_db = boto3.resource('dynamodb')
    user_notes_table = dynamo_db.Table('user-notes')
    
    # Query the user-notes table for notes associated with the user_email
    result = user_notes_table.query(
        KeyConditionExpression=Key('user').eq(user_email),
        Limit=10,  # Limit to 10 notes per query
        ScanIndexForward=False  # Sort by create_date in descending order
    )

    # Check if there are items in the result and return them
    return result.get('Items', [])  # Return an empty list if no notes are found


# Don't modify this function name and arguments
def get_authenticated_user_email(token):
    if not token or len(token) == 0:
        raise InvalidResponse(403)   

    dynamo_db = boto3.resource('dynamodb')
    tokens_table = dynamo_db.Table('token-email-lookup')

    # Validate the given token with one from the database
    response = tokens_table.get_item(
        Key={'token': token}
    )
    
    # Check if the item exists and return user email if the tokens match
    if 'Item' in response:  # Corrected from 'item' to 'Item'
        return response['Item']['email']  # Accessing email from Item
    else:
        raise InvalidResponse(403)  # Changed to 403 for unauthorized access


def authenticate_user(headers):
    authentication_header = headers.get('Authentication', '')

    # Validate the Authentication header format
    if not authentication_header.startswith("Bearer "):
        raise InvalidResponse(400)  # Return 400 for malformed or missing header

    token = authentication_header.split(" ")[1].strip()  # Extract token

    user_email = get_authenticated_user_email(token)

    return user_email


def build_response(status_code, body=None):
    result = {
        'statusCode': str(status_code),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }
    
    if body is not None:
        result['body'] = json.dumps(body)  # Ensure body is serialized to JSON format

    return result


# Don't modify handler, make other functions fit it
def handler(event: dict, context):
    try:
        user_email = authenticate_user(event['headers'])
        notes = query_user_notes(user_email)
    except InvalidResponse as e:
        return build_response(status_code=e.status_code)
    else:
        return build_response(
            status_code=200,
            body=notes  # Directly returning notes as they are already structured data
        )
