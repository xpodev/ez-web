from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

import ez

from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware

from .context import get_current_session, close_session
from .requests import LoginRequest

from .authentication import authenticate


admin = ez.web.http.router("/admin", middleware=[Middleware(SessionMiddleware, secret_key="ez-admin")])


@admin.post("/login")
async def login(request: Request):
    async with request.form() as form:
        login = LoginRequest.model_validate(form)

        session = authenticate(login.username, login.password)
        if session is None:
            raise ez.web.http.HTTPException(ez.web.http.HTTPStatus.UNAUTHORIZED, "Invalid credentials")

        request.session["ez-admin:sid"] = session.id

        return JSONResponse({"message": "Logged in"})
    

@admin.post("/logout")
def logout(request: Request):
    session = get_current_session()
    if close_session(session):
        del request.session["ez-admin:sid"]
    return JSONResponse({"message": "Logged out"})
    

@admin.get("/test")
def test(request: Request):
    session = get_current_session()
    return PlainTextResponse(
        session.id + " :: " + str(session.user)
    )
