from ..app.ez_app import EZApplication
from ..startup import ez_init


def main():
    ez_init.app = EZApplication()

    import ez.lowlevel

    ez.lowlevel.APP_HOST = ez_init.app.app_host
    ez.lowlevel.EZ_APP = ez_init.app
    ez.lowlevel.WEB_APP = ez_init.app.web_app

    ez_init.app.run()

    import ez.events as _
