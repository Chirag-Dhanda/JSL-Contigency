class VectorDBError(Exception):
    """Base class for all Vector DB related errors."""
    pass

class VectorDBConnectionError(VectorDBError):
    """Raised when the connection to the vector database fails."""
    pass

class VectorDBConfigurationError(VectorDBError):
    """Raised when there is an issue with vector database configuration."""
    pass

class VectorDBStorageError(VectorDBError):
    """Raised when there are storage or permission issues for persistence."""
    pass

class VectorDBCollectionError(VectorDBError):
    """Raised when an operation on a specific collection fails."""
    pass
