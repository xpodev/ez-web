import yaml
import ez

from . import configs
from .constants import CONFIG_FILENAME


config = None


def load_config(filename: str):
    with open(filename, "r") as file:
        config: dict = yaml.safe_load(file)
        version = config.get("version", None)
        if version is None:
            raise ValueError("Site config version is not specified")
        if not configs.is_version_supported(version):
            raise ValueError(f"Unsupported site config version: v{version}")
        config_class = configs.get_config_class(version)
        return config_class.model_validate(config)


def load():
    global config
    config_file = ez.SITE_DIR / CONFIG_FILENAME
    config = load_config(str(config_file.resolve()))
