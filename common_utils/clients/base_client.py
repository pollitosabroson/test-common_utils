import logging
from json import JSONDecodeError

import requests

logger = logging.getLogger(__name__)


class BaseClient:
    @staticmethod
    def make_request(
        service_name: str,
        request_url: str,
        data: dict,
        method: str = "GET",
        timeout: int = 60,
        headers: dict = {},
        process_response: bool = True,
    ):

        method_func = {
            "GET": requests.get,
            "POST": requests.post,
            "DELETE": requests.delete,
            "PUT": requests.put,
        }

        try:
            request = method_func[method.upper()](
                request_url, json=data, timeout=timeout, headers=headers
            )
        except requests.exceptions.ConnectTimeout:
            raise Exception(
                status=requests.codes.REQUEST_TIMEOUT,
                description=(
                    f"Timeout request ({timeout}s) on "
                    f"{service_name} (URL: {request_url})."
                ),
            )
        except requests.exceptions.ConnectionError:
            raise Exception(
                status=requests.codes.SERVICE_UNAVAILABLE,
                description=(
                    f"Failed to connect to {service_name} "
                    f"service (URL: {request_url})."
                ),
            )

        if 200 <= request.status_code <= 299:
            return request.json() if process_response else request
        try:
            error_message = request.json()
            if "message" in error_message:
                raise Exception(
                    status=request.status_code,
                    description=(
                        f"Service {service_name} returned "
                        f"{request.status_code}: {error_message['message']}."
                    ),
                )
            else:
                raise Exception(
                    status=request.status_code,
                    description=(
                        f"Service {service_name} "
                        f"returned {request.status_code}."
                    ),
                )
        except JSONDecodeError:
            logger.error(f"Bad response info: {request.content}")
            raise Exception(
                status=request.status_code,
                description=f"Bad response from {request.content}.",
            )
