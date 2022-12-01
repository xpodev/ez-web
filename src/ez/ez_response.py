from json import dumps


class _EzResponse:
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
        self._headers[key] = value
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

    @property
    def headers(self):
        """
        The headers of the response.
        """
        return self._headers

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
