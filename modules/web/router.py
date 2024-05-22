from starlette.routing import Router


class EZRouter(Router):
    def add_router(self, route: str, router: Router):
        self.mount(route, router)

    def _decorator(self, route: str, methods: list[str], **kwargs):
        def decorator(func):
            return self.add_route(route, func, methods=methods, **kwargs)
        
        return decorator

    def get(self, route: str, **kwargs):
        return self._decorator(route, ["GET"], **kwargs)
    
    def post(self, route: str, **kwargs):
        return self._decorator(route, ["POST"], **kwargs)
    
    def put(self, route: str, **kwargs):
        return self._decorator(route, ["PUT"], **kwargs)
    
    def delete(self, route: str, **kwargs):
        return self._decorator(route, ["DELETE"], **kwargs)
    
    def patch(self, route: str, **kwargs):
        return self._decorator(route, ["PATCH"], **kwargs)
    
    def options(self, route: str, **kwargs):
        return self._decorator(route, ["OPTIONS"], **kwargs)
    
    def head(self, route: str, **kwargs):
        return self._decorator(route, ["HEAD"], **kwargs)
    
    def trace(self, route: str, **kwargs):
        return self._decorator(route, ["TRACE"], **kwargs)
    
    def connect(self, route: str, **kwargs):
        return self._decorator(route, ["CONNECT"], **kwargs)
    
    def all(self, route: str, **kwargs):
        return self._decorator(route, ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"], **kwargs)
