import json

from db_service import get_item
from request_validation_utils import validate_property_exist
from request_response_utils import return_error_response, return_status_ok

ENV_TABLE_NAME = "dermoapp-doctor"


def handler(event, context):
    try:
        print("lambda execution with context {0}".format(str(context)))
        if validate_property_exist("doctor_id", event['pathParameters']):
            doctor_id = event['pathParameters']['doctor_id']
            response = get_item("doctor_id", doctor_id)
            return return_status_ok(response)
        else:
            return return_error_response("missing or malformed request body", 412)
    except Exception as err:
        return return_error_response("cannot proceed with the request error: " + str(err), 500)

