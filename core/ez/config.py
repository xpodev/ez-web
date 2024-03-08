from dataclasses import dataclass
import os
from pathlib import Path
import yaml


from utilities.uri import UnifiedResourceIdentifier


SITE_CONFIG_FILENAME = "site.yaml"


class Config:
    def __init__(self, config_file):
        self.config_file = Path(config_file)
        if not self.config_file.is_file():
            raise FileNotFoundError(f"Config file '{self.config_file}' not found.")
        self.config = yaml.safe_load(open(self.config_file))
        self.database = self._load_database_config()

    def reload(self):
        if hasattr(self, "config"):
            for key in list(self.config.env):
                os.environ.pop(key, None)
        self.config = yaml.safe_load(open(self.config_file))
        for key, value in self.config.env.items():
            os.environ[key] = value

        self._load_database_config()

    def _load_database_config(self):
        if "database" not in self.config:
            raise KeyError("Database configuration not found in config file.")

        database_config = self.config["database"]
        if "uri" in database_config:
            return DatabaseConfig.from_uri(**database_config)

        return DatabaseConfig(**database_config)


@dataclass
class DatabaseConfig:
    driver: str
    username: str
    password: str
    host: str
    port: int
    database: str
    prefix: str = ""
    name: str = ""

    @property
    def uri(self):
        return (
            f"{self.driver}://"
            + f"{self.username}:{self.password}@"
            + f"{self.host}:{self.port}"
            + f"{self.database}"
        )

    @staticmethod
    def from_uri(uri: str, **config):
        _uri = UnifiedResourceIdentifier.safe_parse(uri)
        if _uri.authority is None:
            raise ValueError(f"DB URI must provide host information")
        return DatabaseConfig(
            driver=_uri.scheme,
            username=_uri.authority.userinfo.username,
            password=_uri.authority.userinfo.password,
            host=_uri.authority.host,
            port=_uri.authority.port,
            database=_uri.path,
            **config,
        )


config = Config(SITE_CONFIG_FILENAME)

del yaml
del Config
