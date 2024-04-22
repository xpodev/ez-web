from sqlalchemy import Column, String, Boolean, Integer

from ez.data.database import *

from .installer import EZPluginInstaller
from .loader import EZPluginLoader


class PluginInfoModel(DatabaseModel):
    __tablename__ = "plugins"

    id: int = Column(Integer, primary_key=True, autoincrement=True)  # type: ignore
    package_name: str = Column(String, nullable=False, unique=True)  # type: ignore

    name: str = Column(String, nullable=False)  # type: ignore
    description: str = Column(String, nullable=True, default="No description provided.")  # type: ignore
    author: str = Column(String, nullable=False)  # type: ignore
    version: str = Column(String, nullable=False)  # type: ignore

    enabled: bool = Column(Boolean, nullable=False, default=False)  # type: ignore

    home_page: str = Column(String, nullable=True, default="")  # type: ignore

    installer_id: str = Column(String, name="installer", nullable=False, default=EZPluginInstaller.info.id)  # type: ignore
    default_loader_id: str = Column(String, name="default_loader", nullable=True, default=EZPluginLoader.info.id)  # type: ignore

    __ez_id_column__ = package_name  # type: ignore


PluginRepository = DatabaseRepository.create_type(PluginInfoModel)

PLUGIN_REPOSITORY = PluginRepository()
