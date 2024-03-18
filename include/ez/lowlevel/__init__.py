from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sandbox.host.app_host import AppHost
    from core.app.ez_app import EZApplication
    from core.web.applications import EZWebApplication


APP_HOST: "AppHost"

EZ_APP: "EZApplication"
WEB_APP: "EZWebApplication"
