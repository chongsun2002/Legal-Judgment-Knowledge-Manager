class InvalidMetadataKeyException(Exception):
    def __init__(self, message: str = "An invalid metadata key was provided.\nValid keys: case_name, citation, year, parties."):
        super().__init__(message)

class InvalidMetadataFormatException(Exception):
    def __init__(self, message: str = 'An invalid metadata format was provided.\nValid example: {"year": 2020, "case_name": "Public Prosecutor"}'):
        super().__init__(message)