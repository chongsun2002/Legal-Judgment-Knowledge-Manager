class DuplicateJudgmentException(Exception):
    def __init__(self, message: str = "Judgment already exists in storage."):
        super().__init__(message)

class JudgmentNotFoundException(Exception):
    def __init__(self, message: str = "The requested judgment could not be found in the storage."):
        super().__init__(message)

class NoMatchingJudgmentException(Exception):
    def __init__(self, message: str = "No judgments fulfilling the search query could be found in the storage."):
        super().__init__(message)