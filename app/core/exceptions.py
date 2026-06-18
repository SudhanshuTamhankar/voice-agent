class BaseAppException(Exception):
    """Base exception for the application."""
    pass

class MissingDatasetError(BaseAppException):
    """Raised when a required dataset file is missing from the Dataset/ directory."""
    pass

class DatasetParsingError(BaseAppException):
    """Raised when a row in a dataset fails schema validation or cannot be parsed."""
    pass

class EntityNotFoundError(BaseAppException):
    """Raised when an entity (like Institute) is not found in the repositories."""
    pass
