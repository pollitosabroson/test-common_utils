from errors.handling_errors import ExternalConnection, QueryError


def response_verifier(response, service, value):
    """
    Catch microservice response
    :param response: Dictionary with microservice response
    :param service: String with service called
    :param value: String value that we want to get
    :return: Microservice response
    """
    if response:
        if response.get("data"):
            if not response.get("data").get(service).get("success"):
                raise ExternalConnection(
                    response.get("data").get(service).get("errors")
                )
            return response.get("data").get(service).get(value)
    errors = [error.get("message") for error in response.get("errors")]
    raise QueryError(errors)
