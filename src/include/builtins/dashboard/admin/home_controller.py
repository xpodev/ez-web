from fastapi import Request

import ez
from ez.pyx import *
import ez.log as log
from ez.database import select, session
from ez.database.models.user import UserModel
from ez.database.models.plugin import PluginModel

from .security import login
from .components.plugin_list import PluginList


def auth_middle(request: Request, response, next):
    if request.cookies.get("user_id"):
        # because we use jwt, we can trust the user_id
        request.scope["user"] = UserModel.get(request.cookies["user_id"])
        return next()

    ez.response.status(307)
    ez.response.header("Location", f"/admin/login?redirect={request.url.path}")


admin_home_router = ez.router("/admin", middleware=[auth_middle])


@admin_home_router.get("/")
def layout(request):
    return Page(
        Div(
            H1("Dashboard Admin"),
            P("This is the admin dashboard"),
            P("You can add more stuff here"),
        ),
        Script(src="/static/admin/login.js"),
    )


@admin_home_router.get("/plugins")
def plugin_page(request):
    plugins = select(PluginModel)
    return Page(
        PluginList(session.scalars(plugins)),
    )


@ez.post("/admin/login")
async def login_request(request: Request):
    data = await request.json()
    if login(data["username"], data["password"]):
        ez.response.status(200)
    else:
        ez.response.status(401)


@ez.get("/admin/login")
def login_page(request: Request):
    return Page(
        Div(
            H1("Login"),
            Form(
                Label("Username: ", html_for="username"),
                Input(type="text", name="username", class_name="form-control"),
                Label("Password: ", html_for="password"),
                Input(type="password", name="password", class_name="form-control"),
                Button("Login", type="submit", class_name="btn btn-primary"),
                id="login-form",
            ),
            class_name="container w-50 mx-auto card p-3"
        ),
        Script(src="/static/admin/login.js"),
    )


@admin_home_router.get("/logout")
def logout(request: Request):
    ez.response.delete_cookie("user_id")
    ez.response.status(307)
    ez.response.header("Location", "/admin/login")