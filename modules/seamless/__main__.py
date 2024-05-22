from starlette.responses import HTMLResponse
import ez

from ez.web.responses import response_for

from seamless.middlewares import ASGIMiddleware
from seamless.renderer import render
from seamless import Component, Element

@response_for(lambda x: isinstance(x, (Element, Component)))
def jsx_response(x):
    return HTMLResponse(render(x))


ez.lowlevel.WEB_APP.add_middleware(ASGIMiddleware)

__module_name__ = "EZ JSX Integration"
