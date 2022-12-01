from ez import Ez
from ez.events import HTTP
from fastapi import Request


@Ez.on(HTTP.In)
def on_http_in(request: Request):
    Ez.emit(HTTP[request.method], request)
