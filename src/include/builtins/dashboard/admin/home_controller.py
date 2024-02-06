import ez
from ez.html import *
from ez.html.components import Page

admin_home_router = ez.router("/admin")


@admin_home_router.get("/")
def layout(request):
    return Page(
        Div(
            H1("Dashboard Admin"),
            P("This is the admin dashboard"),
            P("You can add more stuff here"),
        )
    )
