import json


def return_error_response(error_message, http_code):
    return {
        "statusCode": http_code,
        "body": json.dumps(
            {
                "message": error_message
            }
        ),
    }


def return_status_ok(response_body):
    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
    }

