import ez

from pydantic.fields import FieldInfo

from ez.plugins import Settings

from seamless.html import Div
from seamless.styling import Style


def render_settings_viewer(settings: Settings):
    def render_section(section: type[Settings], value: Settings):
        return Div()(
            Div()(section.__ez_section_title__),
            render_settings_viewer(value)
        )

    def render_field(name: str, field: FieldInfo, value):
        annotation = field.annotation
        if not isinstance(annotation, type):
            raise TypeError
        provider_type = ez.data.providers.get_provider_type(annotation)
        provider = provider_type.load(value)
        return Div(style=Style(
            display="flex",
            flexDirection="column"
        
        ))(
            (field.title or name) + ": ",
            provider.render_input()
        )

    return Div()(
        *[
            render_section(field.annotation, getattr(settings, name))
            if isinstance(field.annotation, type) and issubclass(field.annotation, Settings)
            else render_field(name, field, getattr(settings, name))
            for name, field in settings.model_fields.items()
        ]
    )
