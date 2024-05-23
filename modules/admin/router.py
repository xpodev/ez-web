from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

import ez

from .context import get_current_session, close_session
from .requests import LoginRequest

from .authentication import authenticate


admin = ez.web.http.router("/admin")


@admin.post("/login")
async def login(request: Request):
    async with request.form() as form:
        login = LoginRequest.model_validate(form)

        return JSONResponse({"message": "Logged in"})
    

@admin.post("/logout")
def logout(request: Request):
    session = get_current_session()
    close_session(session)
    return JSONResponse({"message": "Logged out"})
    
