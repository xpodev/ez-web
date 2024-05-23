from typing import Any, Callable, Concatenate, ParamSpec, TypeAlias, TypeVar, SupportsIndex, overload


_EMPTY: Any = object()

MenuID: TypeAlias = str

P = ParamSpec("P")
MenuEntryT = TypeVar("MenuEntryT", bound="MenuEntry")
MenuEntryCls = Callable[Concatenate["Menu", MenuID, P], MenuEntryT]



class MenuEntry:
    _parent: "Menu | None"

    def __init__(self, parent: "Menu | None", id: str | None = None):
        self._parent = parent
        self._id = id

    @property
    def menu(self):
        return self._parent
    
    @property
    def id(self):
        return self._id


class Menu(MenuEntry):
    _entries: list[MenuEntry]
    _mapping: dict[MenuID, MenuEntry]

    def __init__(self, parent: "Menu | None"):
        super().__init__(parent)

        self._entries = []
        self._mapping = {}

    def add_entry(self, entry: MenuEntry) -> None:
        self._entries.append(entry)
        if entry.id is not None:
            self._mapping[entry.id] = entry

    def add_entry_at(self, index: SupportsIndex, entry: MenuEntry) -> None:
        self._entries.insert(index, entry)
        if entry.id is not None:
            self._mapping[entry.id] = entry

    def add_entries(self, *entries: MenuEntry) -> None:
        for entry in entries:
            self.add_entry(entry)

    def add_entries_at(self, index: SupportsIndex, *entries: MenuEntry) -> None:
        index = index.__index__()
        for i, entry in enumerate(entries):
            self.add_entry_at(index + i, entry)

    @overload
    def add_entry_before(self, target: MenuEntry, entry: MenuEntry, /) -> None: ...
    @overload
    def add_entry_before(self, entry_id: MenuID, entry: MenuEntry, /) -> None: ...

    def add_entry_before(self, target: MenuEntry | MenuID, entry: MenuEntry, /):
        if isinstance(target, MenuID):
            target = self._mapping[target]
        index = self._entries.index(target)
        self.add_entry_at(index - 1, entry)

    @overload
    def add_entry_after(self, target: MenuEntry, entry: MenuEntry, /) -> None: ...
    @overload
    def add_entry_after(self, entry_id: MenuID, entry: MenuEntry, /) -> None: ...

    def add_entry_after(self, target: MenuEntry | MenuID, entry: MenuEntry, /):
        if isinstance(target, MenuID):
            target = self._mapping[target]
        index = self._entries.index(target)
        self.add_entry_at(index, entry)

    @overload
    def add_entries_before(self, target: MenuEntry, /, *entries: MenuEntry) -> None: ...
    @overload
    def add_entries_before(self, entry_id: MenuID, /, *entries: MenuEntry) -> None: ...

    def add_entries_before(self, target: MenuEntry | MenuID, /, *entries: MenuEntry):
        if isinstance(target, MenuID):
            target = self._mapping[target]
        index = self._entries.index(target)
        self.add_entries_at(index - 1, *entries)

    @overload
    def add_entries_after(self, target: MenuEntry, /, *entries: MenuEntry) -> None: ...
    @overload
    def add_entries_after(self, entry_id: MenuID, /, *entries: MenuEntry) -> None: ...

    def add_entries_after(self, target: MenuEntry | MenuID, /, *entries: MenuEntry):
        if isinstance(target, MenuID):
            target = self._mapping[target]
        index = self._entries.index(target)
        self.add_entries_at(index, *entries)

    def create_entry(
            self, 
            cls: MenuEntryCls[P, MenuEntryT], 
            *args: P.args, 
            **kwargs: P.kwargs
            ) -> MenuEntryT:
        entry = cls(self, *args, **kwargs)
        self.add_entry(entry)
        return entry
    
    def create_entry_at(
            self, 
            index: SupportsIndex, 
            cls: MenuEntryCls[P, MenuEntryT],
            *args: P.args,
            **kwargs: P.kwargs
            ) -> MenuEntryT:
        entry = cls(self, *args, **kwargs)
        self._entries.insert(index, entry)
        return entry
    
    @overload
    def entry_at(self, index: SupportsIndex, /) -> MenuEntry: ...
    @overload
    def entry_at(self, index: SupportsIndex, entry: MenuEntry, /) -> None: ...

    def entry_at(self, index: SupportsIndex, entry: MenuEntry | None = _EMPTY, /):
        if entry is _EMPTY:
            return self[index]
        if entry is None:
            del self[index]
        else:
            self[index] = entry

    def remove_entry(self, entry: MenuEntry) -> None:
        del self[entry]

    def remove_entry_at(self, index: SupportsIndex) -> None:
        del self[index]

    @overload
    def index(self, entry: MenuEntry, /) -> int: ...
    @overload
    def index(self, entry_id: MenuID, /) -> int: ...

    def index(self, entry: MenuEntry | MenuID, /) -> int:
        if isinstance(entry, MenuID):
            entry = self._mapping[entry]
        return self._entries.index(entry)

    @overload
    def __contains__(self, entry: MenuEntry, /) -> bool: ...
    @overload
    def __contains__(self, entry_id: MenuID, /) -> bool: ...

    def __contains__(self, entry: MenuEntry | MenuID, /) -> bool:
        if isinstance(entry, MenuID):
            return entry in self._mapping
        return entry in self._entries

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> MenuEntry: ...
    @overload
    def __getitem__(self, entry_id: MenuID, /) -> MenuEntry: ...

    def __getitem__(self, index_or_id: SupportsIndex | MenuID) -> MenuEntry:
        if isinstance(index_or_id, MenuID):
            return self._mapping[index_or_id]
        return self._entries[index_or_id]
    
    @overload
    def __setitem__(self, index: SupportsIndex, entry: MenuEntry, /) -> None: ...
    @overload
    def __setitem__(self, entry_id: MenuID, entry: MenuEntry, /) -> None: ...

    def __setitem__(self, index: SupportsIndex | MenuID, entry: MenuEntry, /):
        if isinstance(index, MenuID):
            index = self.index(index)
        self._entries[index] = entry

    @overload
    def __delitem__(self, index: SupportsIndex, /) -> None: ...
    @overload
    def __delitem__(self, entry_id: MenuID, /) -> None: ...
    @overload
    def __delitem__(self, entry: MenuEntry, /) -> None: ...

    def __delitem__(self, entry: SupportsIndex | MenuEntry | MenuID, /):
        if not isinstance(entry, MenuEntry):
            entry = self[entry]
        self._entries.remove(entry)
        if entry.id is not None:
            del self._mapping[entry.id]

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)


__all__ = [
    "Menu",
    "MenuEntry"
]
