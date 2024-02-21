from sqlalchemy import Column, String, Boolean, Integer

from data.database import *

from .installer import EZPluginInstaller


class PluginInfoModel(DatabaseModel):
    __tablename__ = "plugins"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    version: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True, default="No description provided.")
    installer_id: str = Column(String, name="installer", nullable=False, default=EZPluginInstaller.info.id)
    package_name: str = Column(String, nullable=False, unique=True)
    author: str = Column(String, nullable=False)
    enabled: bool = Column(Boolean, nullable=False, default=False)

    __ez_id_column__ = package_name


PluginRepository = DatabaseRepository.create_type(PluginInfoModel)

PLUGIN_REPOSITORY = PluginRepository()
