from json import dumps
from typing import Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response


class EZResponse:
    def __init__(self):
        self._headers = {}
        self._status_code = 0
        self._body = None

    def status(self, code):
        """
        Sets the status code of the response.

        :param code: The status code to set.

        :return: The response object.
        """
        self._status_code = code
        return self

    def header(self, key, value):
        """
        Sets a header in the response.

        :param key: The key of the header.
        :param value: The value of the header.

        :return: The response object.
        """
        key = self._format_header(key)
        if self._headers.get(key):
            self._headers[key].append(value)
        else:
            self._headers[key] = [value]
        return self

    def json(self, data):
        """
        Sets the response body to a JSON string and sets the `Content-Type` header to `application/json`.
        If the status code is not set, it will be set to 200.

        :param data: The data to convert to JSON.

        :return: The response object.
        """
        self.header("Content-Type", "application/json")
        if self._status_code == 0:
            self.status(200)
        self._body = dumps(data)
        return self

    def text(self, data):
        """
        Sets the response body to a string and sets the `Content-Type` header to `text/plain`.
        If the status code is not set, it will be set to 200.

        :param data: The data to set as the response body.

        :return: The response object.
        """
        self.header("Content-Type", "text/plain")
        if self._status_code == 0:
            self.status(200)
        self._body = data
        return self

    def html(self, data):
        """
        Sets the response body to a string and sets the `Content-Type` header to `text/html`.
        If the status code is not set, it will be set to 200.

        :param data: The data to set as the response body.

        :return: The response object.
        """
        self.header("Content-Type", "text/html")
        if self._status_code == 0:
            self.status(200)
        self._body = data
        return self

    def cookie(self, key, value, **kwargs):
        """
        Sets a cookie in the response.

        :param key: The key of the cookie.
        :param value: The value of the cookie.
        :param kwargs: Additional cookie parameters.

        :return: The response object.
        """
        self.header(
            "Set-Cookie",
            f"{key}={value}; {'; '.join(f'{k}={v}' for k, v in kwargs.items())}",
        )
        return self

    def delete_cookie(self, key):
        """
        Deletes a cookie in the response.

        :param key: The key of the cookie to delete.

        :return: The response object.
        """
        self.header("Set-Cookie", f"{key}=; Max-Age=0")
        return self

    @property
    def headers(self):
        """
        The headers of the response.
        """
        return {
            k: ", ".join(v) if isinstance(v, list) else v
            for k, v in self._headers.items()
        }

    @property
    def status_code(self):
        """
        The status code of the response.
        """
        return 200 if self._status_code == 0 else self._status_code

    @property
    def body(self):
        """
        The body of the response.
        """
        return self._body

    def _format_header(self, key: str):
        """
        Formats a header key to be title case.
        """
        return "-".join([i.capitalize() for i in key.split("-")])

    def _auto_body(self, data):
        """
        Automatically sets the response body based on the type of the data.
        """
        from ez.database.models import Model

        match data:
            case dict() | int() | float() | bool():
                return self.json(data)
            case list():
                return self.json(
                    list(
                        map(
                            lambda x: (
                                jsonable_encoder(x) if isinstance(x, Model) else x
                            ),
                            data,
                        )
                    )
                )
            case str():
                return self.text(data)
            case Model():
                return self.json(jsonable_encoder(data))
            case _:
                self._body = data
                return self

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Response(
            content=self.body,
            status_code=self.status_code,
            headers=self.headers,
        )