import uvicorn
from fastapi import FastAPI, Request, Response

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.ez import Ez
from core.compile_tree import compile_tree
from include.plugin_loader import load_plugins

docs_urls = [
    "/docs",
    "/redoc",
    "/openapi.json",
]

app = FastAPI()

load_plugins()
Ez.emit("plugins.loaded")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        Ez.reload_tree()
        Ez.response.html("")
        if request.url.path in docs_urls:
            return await call_next(request)
        Ez.emit("request", request)
        Ez.request = request

        Ez.emit(f"{request.method}[{request.url.path}]", request)
        Ez.emit("compiler.init", Ez.tree.tree)

        if Ez.response.headers.get("Content-Type") == "text/html":
            Ez.response.html(compile_tree(Ez.tree.tree))

        return Response(
            content=Ez.response.body,
            headers=Ez.response.headers,
            status_code=Ez.response.status_code
        )


app.add_middleware(RequestContextMiddleware)   

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
