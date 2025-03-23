from flask_restx import reqparse
from exceptions.data_validation_exceptions import InvalidMetadataKeyException

def get_judgments_parser():
    judgment_parser = reqparse.RequestParser()
    judgment_parser.add_argument(
        'metadata',
        type=str,
        required=False,
        help='Optional JSON-style filter. '
        'Valid keys: case_name, citation, year, parties.\n'
        'Example: metadata={"year": 2020, "case_name": "Public Prosecutor"}'
    )
    return judgment_parser

get_judgments_responses = {
    200: 'ZIP file of all or filtered judgments',
    400: 'Invalid metadata format',
    404: 'No matching judgments found',
    415: 'Invalid metadata format'
}

get_judgments_id_params = {
    'id': 'Unique judgment ID'
}

get_judgments_id_responses = {
    200: 'Judgment with the id, as a pdf file',
    404: 'Judgment not found'
}

ALLOWED_METADATA_KEYS = {"case_name", "citation", "year", "parties"}

def validate_metadata(metadata: dict):
    invalid_keys = set(metadata.keys()) - ALLOWED_METADATA_KEYS
    if invalid_keys:
        raise InvalidMetadataKeyException()
    