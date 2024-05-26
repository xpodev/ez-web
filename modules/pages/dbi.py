from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from ez.data.database import DatabaseModel, DatabaseRepository


class PageInfoModel(DatabaseModel):
    __tablename__ = "pages"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    config: str = Column(String)
    slug: str = Column(String)
    template_name: str = Column(String)

    __ez_id_column__ = id


class PagesHistoryModel(DatabaseModel):
    __tablename__ = "pages_history"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=True)
    page_id: int = Column(Integer, nullable=False)
    content_data: str = Column(String)
    date: datetime = Column(DateTime, default=datetime.now)

    __ez_id_column__ = id


PageRepository = DatabaseRepository.create_type(PageInfoModel)
PagesHistoryRepository = DatabaseRepository.create_type(PagesHistoryModel)

PAGE_REPOSITORY = PageRepository()
PAGES_HISTORY_REPOSITORY = PagesHistoryRepository()
