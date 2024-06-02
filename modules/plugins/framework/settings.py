from typing import Any, ClassVar, Unpack

from pydantic import BaseModel, ConfigDict

from utilities.utils import spacify


_EMPTY: Any = object()


class Settings(BaseModel):
    __ez_section_title__: ClassVar[str | None]
    __ez_section_id__: ClassVar[str | None]

    def __init_subclass__(cls, *, section: str = _EMPTY, section_id: str = _EMPTY, **kwargs: Unpack[ConfigDict]):
        super().__init_subclass__(**kwargs)

        if section is _EMPTY and section_id is _EMPTY:
            section = spacify(cls.__name__)
        
        if section_id is _EMPTY:
            section_id = section.lower().replace(' ', '-')
        elif section is _EMPTY:
            section = section_id.replace('-', ' ').title()
        
        cls.__ez_section_title__ = section
        cls.__ez_section_id__ = section_id
