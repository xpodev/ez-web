from dataclasses import dataclass


@dataclass(frozen=True)
class PageData:
    id: int
    title: str
    content: str
    slug: str
    template_name: str
