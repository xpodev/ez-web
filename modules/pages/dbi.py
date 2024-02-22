from sqlalchemy import Column, Integer, String, ForeignKey

from data.database import DatabaseModel, DatabaseRepository


class PageInfoModel(DatabaseModel):
    __tablename__ = "pages"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    content: str = Column(String)
    slug: str = Column(String)
    template_name: str = Column(String)


PageRepository = DatabaseRepository.create_type(PageInfoModel)
PAGE_REPOSITORY = PageRepository()
