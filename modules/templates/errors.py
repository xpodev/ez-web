from ez.errors import EZError


class EZTemplateError(EZError):
    pass


class TemplateNotFoundError(EZTemplateError):
    name: str

    def __init__(self, name: str) -> None:
        super().__init__(f"Template '{name}' not found")
        self.name = name
