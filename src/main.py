# from ez import 
import ez
from include.plugins_loader import load_plugins


load_plugins()

app = ez._app

if __name__ == "__main__":
    ez.run()
