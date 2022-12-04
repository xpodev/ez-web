# from ez import ez
import ez
from ez.events import HTTP
from fastapi import Request


@ez.on(HTTP.In)
def on_http_in(request: Request):
    ez.emit(HTTP[request.method], request)
