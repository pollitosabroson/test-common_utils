from utils.constants import ERROR_COLLECTION_EMPTY, VALUE_DONT_EXISTS


class CollectionNameEmpty(Exception):
    """Exception raised for errors in case collection is empty.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args: object, message=ERROR_COLLECTION_EMPTY) -> None:
        self.message = message
        super().__init__(self.message)


class ValueDontExists(Exception):
    """Exception raised for errors in case value dont exists.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args: object, message=VALUE_DONT_EXISTS) -> None:
        self.message = message
        super().__init__(self.message)


class ExternalConnection(Exception):
    """Exception raised for errors in case iot conection fails.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class QueryError(Exception):
    """Exception raised for errors in case value dont exists.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class DefaultError(Exception):
    """Exception raised for errors in case the fail."""
