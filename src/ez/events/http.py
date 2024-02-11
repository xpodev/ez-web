from .event import Event


class HTTP(Event):
    In = "HTTP.In"
    """
    Called when a HTTP request is received.

    :param request: The request object.
    """
    Out = "HTTP.Out"
    """
    Called when a HTTP response is sent.

    :param request: The request object.
    """

    GET = "HTTP.GET"
    """
    Called when a HTTP GET request is received.

    :param request: The request object.
    """
    POST = "HTTP.POST"
    """
    Called when a HTTP POST request is received.

    :param request: The request object.
    """
    PUT = "HTTP.PUT"
    """
    Called when a HTTP PUT request is received.

    :param request: The request object.
    """
    DELETE = "HTTP.DELETE"
    """
    Called when a HTTP DELETE request is received.

    :param request: The request object.
    """
    PATCH = "HTTP.PATCH"
    """
    Called when a HTTP PATCH request is received.

    :param request: The request object.
    """
    HEAD = "HTTP.HEAD"
    """
    Called when a HTTP HEAD request is received.

    :param request: The request object.
    """
    OPTIONS = "HTTP.OPTIONS"
    """
    Called when a HTTP OPTIONS request is received.

    :param request: The request object.
    """
    TRACE = "HTTP.TRACE"
    """
    Called when a HTTP TRACE request is received.

    :param request: The request object.
    """
    CONNECT = "HTTP.CONNECT"
    """
    Called when a HTTP CONNECT request is received.

    :param request: The request object.
    """
