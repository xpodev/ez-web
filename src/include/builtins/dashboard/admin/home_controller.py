from fastapi import Request

import ez
from ez.pyx import *
import ez.log as log

def auth_middle(request: Request, response, next):
    log.info("Auth middleware")
    if request.query_params.get("a") == "1":
        return next()
    
    response.status(401)


admin_home_router = ez.router("/admin", middleware=[auth_middle])


@admin_home_router.get("/")
def layout(request):
    return Page(
        Div(
            H1("Dashboard Admin"),
            P("This is the admin dashboard"),
            P("You can add more stuff here"),
        ),
        Script(
            src="/static/admin/admin.js"
        )
    )
