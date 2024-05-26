from typing import Any as Renderable, ClassVar, Generic, Self, TypeAlias, TypeVar, cast

from pydantic import BaseModel, create_model

from seamless.html import Label

from ..configurable import Configurable


T = TypeVar("T")
Config = TypeVar("Config", bound=BaseModel)


_DataProviderType: TypeAlias = "type[DataProviderBase]"


class _DataProviderRegistry:
    class _Entry:
        default: _DataProviderType
        providers: list[_DataProviderType]

        def __init__(self, default: _DataProviderType) -> None:
            self.default = default
            self.providers = []

        def add(self, provider: _DataProviderType) -> None:
            self.providers.append(provider)

    _registry: dict[type, _Entry] = {}

    def __init__(self) -> None:
        self._registry = {}

    def get(self, data_type: type) -> _DataProviderType:
        if data_type in self._registry:
            return self._registry[data_type].default
        raise ValueError(f"No data provider found for type {data_type}")

    def register(self, data_type: type, provider: _DataProviderType, *, set_as_default=False) -> None:
        if data_type not in self._registry:
            entry = self._registry[data_type] = self._Entry(provider)
        else:
            entry = self._registry[data_type]
            entry.add(provider)
        if set_as_default:
            entry.default = provider


_DATA_PROVIDER_REGISTRY = _DataProviderRegistry()


class DataProviderBase(Generic[T]):
    """
    Base class for data providers.

    Data providers are used to provide data to templates.
    """

    __ez_data_type__: type[T] | None
    __ez_data_provider__: ClassVar[type["DataProviderBase"] | None] = None

    def __init_subclass__(cls, *, data_type: type[T] | None = None, set_as_default=False, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        
        if data_type is None:
            return
        
        if not isinstance(data_type, type):
            raise TypeError(f"Data type for {cls.__name__} must be a type")

        if data_type is not None:
            cls.__ez_data_type__ = data_type
            cls.__ez_data_provider__ = cls
            _DATA_PROVIDER_REGISTRY.register(data_type, cls, set_as_default=set_as_default)

    def provide(self) -> T:
        """
        Provide data to templates.

        Returns:
            T: Data to provide to templates.
        """
        raise NotImplementedError

    def render_input(self) -> Renderable | str:
        """
        Render input fields for the data provider.

        Returns:
            Renderable: Renderable UI element or an HTML string.
        """
        raise NotImplementedError

    @classmethod
    def load(cls, config: dict) -> Self:
        """
        Load a data provider from a configuration dictionary.

        Override this method to change how data providers are constructed.

        Args:
            config (dict): Configuration dictionary.

        Returns:
            Self: Loaded data provider.
        """
        raise NotImplementedError

    @classmethod
    def default(cls) -> Self:
        """
        Get the default data provider for the data type.

        Returns:
            Self: Default data provider.
        """
        raise NotImplementedError


class ModelProvider(DataProviderBase[T], Configurable[Config], Generic[T, Config]):
    """
    Base class for data providers.

    Data providers are used to provide data to templates.

    Args:
        config (Config): Configuration for the data provider.
    """

    __ez_config_type__: ClassVar[type[BaseModel]]

    def __init_subclass__(cls, *, config_type: type[Config], **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        cls.__ez_config_type__ = config_type

    def provide(self) -> T:
        """
        Provide data to templates.

        Returns:
            T: Data to provide to templates.
        """
        raise NotImplementedError

    def render_input(self) -> Renderable | str:
        """
        Render input fields for the data provider.

        Returns:
            Renderable: Renderable UI element or an HTML string.
        """
        for name, field in self.__ez_config_type__.model_fields.items():
            field_type = field.annotation
            if field_type is None:
                continue
            provider = _DATA_PROVIDER_REGISTRY.get(field_type)
            data = getattr(self.config, name)

            field_input = provider.load(data).render_input()
            field_input.props["name"] = name

            yield Label(value=field.alias, for_=name)
            yield field_input

    @classmethod
    def load(cls, config: dict):
        return cls(cast(Config, cls.__ez_config_type__.model_validate(config)))


def get_provider(data_type: type[T], config: Config | None = None) -> DataProviderBase[T]:
    """
    Get the default data provider for a data type.

    Args:
        data_type (type): Data type.

    Returns:
        DataProviderBase: Default data provider for the data type.
    """
    provider = _DATA_PROVIDER_REGISTRY.get(data_type)
    if config is None:
        return provider.default()
    return provider.load(config)


def get_provider_type(data_type: type[T]) -> type[DataProviderBase[T]]:
    """
    Get the default data provider type for a data type.

    Args:
        data_type (type): Data type.

    Returns:
        DataProviderBase: Default data provider type for the data type.
    """
    return _DATA_PROVIDER_REGISTRY.get(data_type)


def get_or_create_provider(data_type: type[T], config: Config) -> DataProviderBase[T] | ModelProvider[T, Config]:
    """
    Get the default data provider for a data type, creating it if it does not exist.

    Args:
        data_type (type): Data type.

    Returns:
        DataProviderBase: Default data provider for the data type.
    """
    try:
        return get_provider(data_type, config)
    except ValueError:
        if not issubclass(data_type, BaseModel):
            data_type = cast(type, create_model("_AutoGeneratedConfig", value=(type(config), config)))
            
        class _AutoGeneratedModelProvider(ModelProvider[data_type, type(config)], data_type=data_type, config_type=type(config)):
            def provide(self):
                return self.config
                
        return _AutoGeneratedModelProvider(config)
