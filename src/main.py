from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.staging")

import ez
from include.plugins_loader import repository as plugins_repository

app = ez._app

if __name__ == "__main__":
    ez.run()
