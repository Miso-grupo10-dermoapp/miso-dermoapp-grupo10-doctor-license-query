import json
import os

import boto3
from boto3.dynamodb.conditions import Key
import moto
import pytest

import app

TABLE_NAME = "Dermoapp-sprint1-doctor-DoctorDetails-HJ34HOQYTKA6"
@pytest.fixture
def lambda_environment():
    os.environ[app.ENV_TABLE_NAME] = TABLE_NAME

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def data_table(aws_credentials):
    with moto.mock_dynamodb():
        client = boto3.client("dynamodb", region_name="us-east-1")
        client.create_table(
            AttributeDefinitions=[
                {"AttributeName": "doctor_id", "AttributeType": "S"},
                {"AttributeName": "license_number", "AttributeType": "S"}
            ],
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "doctor_id", "KeyType": "HASH"},
                {"AttributeName": "license_number", "KeyType": "RANGE"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        yield TABLE_NAME

def test_givenMalformedRequestOnRequestThenReturnError412(lambda_environment, data_table):

    event = {
            "resource": "/doctor/{doctor_id}/license",
            "path": "/doctor/license",
            "httpMethod": "POST",
            "pathParameters": {
            },
            "body": "{\n    \"license_number\": \"234353\" \n}",
            "isBase64Encoded": False
    }
    lambdaResponse = app.handler(event, [])


    assert lambdaResponse['statusCode'] == 412
    assert lambdaResponse['body'] == '{"message": "missing or malformed request body"}'

def test_givenValidRequestAndDBFailureThenReturn500(lambda_environment):

    event = {
            "resource": "/doctor/{doctor_id}/license",
            "path": "/doctor/license",
            "httpMethod": "POST",
            "pathParameters": {
                "doctor_id": "123"
            },
            "body": "{\n    \"license_number\": 234353\n}",
            "isBase64Encoded": False
    }
    lambdaResponse = app.handler(event, [])


    assert lambdaResponse['statusCode'] == 500