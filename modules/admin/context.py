"""
The admin dashboard context module.

The context for the dashboard is composed of multiple layers.

First, the dashboard context is implemented by the ContextRoot class.

The context root then contains a:
- shared context (SharedContext)
- user contexts (UserContext)
- sessions (Session)

The shared context is data that is shared between all logged in users.
The user context is data for a specific user, but shared with all its sessions (open tabs, etc..)
The session context is data for a specific session (connection, tab in browser, etc..)
"""

from typing import TypeAlias, overload
from utilities.utils import bind

from .user import User


SessionID: TypeAlias = str


class SharedContext:
    ...


class SessionContext:
    ...


class UserContext:
    def __init__(self, user: User) -> None:
        self._user = user
        self._sessions = []

    @property
    def user(self) -> User:
        return self._user
    
    @property
    def sessions(self) -> list["Session"]:
        return self._sessions.copy()

    def create_session(self, session_id: str) -> "Session":
        session = Session(self._user, session_id)
        self._sessions.append(session)
        return session
    
    def connect_session(self, session: "Session"):
        if session.user != self._user:
            raise ValueError("Session user does not match user context.")
        self._sessions.append(session)
    
    def disconnect_session(self, session: "Session"):
        try:
            self._sessions.remove(session)
        except ValueError:
            return False
        return True


class Session:   
    def __init__(self, user: User, session_id: SessionID) -> None:
        self._id = session_id
        self._user = user
        self._context = SessionContext()

    @property
    def id(self) -> SessionID:
        return self._id

    @property
    def user(self) -> User:
        return self._user
    
    @property
    def context(self) -> SessionContext:
        return self._context


class ContextRoot:
    _user_contexts: dict[User, UserContext]
    _sessions: dict[SessionID, Session]

    def __init__(self) -> None:
        self._global_context = SharedContext()
        self._user_contexts = {}
        self._sessions = {}

    @property
    def global_context(self) -> SharedContext:
        return self._global_context

    def user_context(self, user: User) -> UserContext:
        if user not in self._user_contexts:
            self._user_contexts[user] = UserContext(user)
        return self._user_contexts[user]
    
    def get_user_context(self, user: User) -> UserContext | None:
        try:
            return self._user_contexts[user]
        except KeyError:
            return None

    def _clear_user_context(self, user: User) -> None:
        try:
            del self._user_contexts[user]
        except KeyError:
            return

    def session(self, session_id: SessionID) -> Session:
        if session_id not in self._sessions:
            raise KeyError(f"Session with ID '{session_id}' not found.")
        return self._sessions[session_id]
    
    def create_session(self, user: User, session_id: str) -> Session:
        session = self.user_context(user).create_session(session_id)
        self._sessions[session_id] = session
        return session
    
    def delete_session(self, session_id: SessionID) -> bool:
        try:
            session = self._sessions.pop(session_id)
        except KeyError:
            return False
        context = self.get_user_context(session.user)

        if context is None:
            return False
        
        result = context.disconnect_session(session)

        if not context.sessions:
            self._clear_user_context(session.user)
        
        return result
    
    def disconnect_user(self, user: User):
        context = self.get_user_context(user)

        if context is None:
            return

        for session in context.sessions:
            self.delete_session(session.id)


_SITE_CONTEXT = ContextRoot()


@bind(_SITE_CONTEXT)
def get_shared_context(ctx: ContextRoot):
    def _get_global_context() -> SharedContext:
        return ctx.global_context
    
    return _get_global_context


@bind(_SITE_CONTEXT)
def get_context_root(ctx: ContextRoot):
    def _get_site_context() -> ContextRoot:
        return ctx
    
    return _get_site_context


@bind(_SITE_CONTEXT)
def get_user_context(ctx: ContextRoot):
    @overload
    def _get_user_context(user: User, /) -> UserContext: ...
    @overload
    def _get_user_context(session: Session, /) -> UserContext: ...
    @overload
    def _get_user_context(session_id: SessionID, /) -> UserContext: ...

    def _get_user_context(value: User | Session | SessionID, /) -> UserContext:
        match value:
            case User() as user:
                result = ctx.get_user_context(user)
                if result is None:
                    raise ValueError("User context not found.")
                return result
            case Session() as session:
                return _get_user_context(session.user)
            case SessionID() as session_id:
                return _get_user_context(ctx.session(session_id))
            case _:
                raise TypeError("Invalid argument type.")
    
    return _get_user_context


@bind(_SITE_CONTEXT)
def create_session(ctx: ContextRoot):
    def _create_session(user: User, session_id: SessionID) -> Session:
        return ctx.create_session(user, session_id)
    
    return _create_session


@bind(_SITE_CONTEXT)
def get_session(ctx: ContextRoot):
    def _get_session(session_id: SessionID) -> Session:
        return ctx.session(session_id)
    
    return _get_session


@bind(_SITE_CONTEXT)
def close_session(ctx: ContextRoot):
    @overload
    def _close_session(session: Session, /) -> bool: ...
    @overload
    def _close_session(session_id: SessionID, /) -> bool: ...

    def _close_session(session_id: Session | SessionID, /) -> bool:
        if isinstance(session_id, Session):
            session_id = session_id.id
        return ctx.delete_session(session_id)
    
    return _close_session


@bind(_SITE_CONTEXT)
def disconnect_user(ctx: ContextRoot):
    def _disconnect_user(user: User):
        ctx.disconnect_user(user)
    
    return _disconnect_user


@bind(_SITE_CONTEXT)
def get_connected_users(ctx: ContextRoot):
    def _get_users() -> list[User]:
        return list(ctx._user_contexts.keys())
    
    return _get_users


del _SITE_CONTEXT
