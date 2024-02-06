from fastapi import FastAPI, Request, APIRouter
from typing import Callable
from .ez_response import _EzResponse
from .ez_router import _EzRouter

response: _EzResponse
request: Request
_app: FastAPI

def __init__(self) -> None:
    # Initialize _Ez instance with proper types
    ...

def add_route(self, route: str, handler: Callable) -> None:
    # Define add_route method with type hints
    ...

def run(self, **kwargs) -> None:
    # Define run method with type hints
    ...

def _run(self, **kwargs) -> None:
    # Define _run method with type hints
    ...

def _setup(self) -> None:
    # Define _setup method with type hints
    ...

def _add_event_handler(self, event: str, k: Callable, v: Callable) -> None:
    # Define _add_event_handler method with type hints
    ...

def get(self, route: str) -> Callable:
    # Define get method with type hints
    ...

# Define other methods with type hints

def router(self, prefix: str = "") -> _EzRouter:
    # Define router method with type hints
    ...

def add_router(self, router: APIRouter) -> None:
    # Define add_router method with type hints
    ...

@property
def _app(self) -> FastAPI:
    # Define _app property with type hints
    ...

def __getattr__(self, name: str) -> None:
    # Define __getattr__ method with type hints
    ...