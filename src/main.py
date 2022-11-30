from ez import Ez
from include.plugins_loader import load_plugins


load_plugins()
Ez.emit("plugins.loaded")

if __name__ == "__main__":
    Ez.run()
