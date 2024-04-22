from io import StringIO, SEEK_CUR
from urllib.parse import urlparse


class URIParser:
    def __init__(self, source: str) -> None:
        self.source = source
        self.stream = StringIO(source)
    
    def parse(self) -> "URI":
        scheme = self._parse_scheme()
        if self.stream.read(2) == "//":
            authority = self._parse_authority()
        else:
            authority = None
            self.stream.seek(-1, SEEK_CUR)
        path = self._parse_path()
        query = self._parse_query()
        fragment = self._parse_fragment()

        return URI(scheme, authority, path, query, fragment, self.source)
    
    def _parse_scheme(self) -> str:
        scheme = ""
        while (char := self.stream.read(1)) != ":":
            scheme += char
        return scheme
    
    def _parse_authority(self) -> "URIAuthority":
        userinfo = self._parse_userinfo()
        host = self._parse_host()
        port = self._parse_port()
        return URIAuthority(userinfo, host, port)
    
    def _parse_userinfo(self) -> "URIUserInfo":
        username = ""
        while (char := self.stream.read(1)) != "@":
            username += char
        password = ""
        while (char := self.stream.read(1)) != ":":
            password += char
        return URIUserInfo(username, password)
    
    def _parse_host(self) -> str:
        host = ""
        while (char := self.stream.read(1)) != ":" and char != "/":
            host += char
        return host
    
    def _parse_port(self) -> int:
        port = ""
        while (char := self.stream.read(1)) != "/":
            port += char
        return int(port)
    
    def _parse_path(self) -> str:
        path = ""
        while (char := self.stream.read(1)) != "?":
            path += char
        return path
    
    def _parse_query(self) -> str:
        query = ""
        while (char := self.stream.read(1)) != "#":
            query += char
        return query
    
    def _parse_fragment(self) -> str:
        return self.stream.read()


class URIUserInfo:
    username: str | None
    password: str | None

    def __init__(self, username: str | None, password: str | None) -> None:
        self.username = username
        self.password = password


class URIAuthority:
    userinfo: URIUserInfo | None
    host: str | None
    port: int | None

    def __init__(self, userinfo: URIUserInfo | None, host: str | None, port: int | None) -> None:
        self.userinfo = userinfo
        self.host = host
        self.port = port


class URIPath:
    SEPARATOR: str = "/"

    raw: str
    segments: list[str]

    def __init__(self, raw: str) -> None:
        self.raw = raw
        self.segments = raw.split(self.SEPARATOR)

    @property
    def name(self) -> str:
        return self.segments[-1]
    
    @property
    def parent(self) -> "URIPath":
        return URIPath(self.SEPARATOR.join(self.segments[:-1]))
    
    def __str__(self) -> str:
        return self.raw
    
    def __truediv__(self, other: str) -> "URIPath":
        return URIPath(self.raw + self.SEPARATOR + other)
    
    def __rtruediv__(self, other: str) -> "URIPath":
        return URIPath(other + self.SEPARATOR + self.raw)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, URIPath):
            return NotImplemented
        return self.raw == other.raw
    
    def __hash__(self) -> int:
        return hash(self.raw)


class URI:
    scheme: str
    authority: URIAuthority | None
    path: str
    query: str
    fragment: str

    raw: str

    def __init__(self, scheme: str, authority: URIAuthority | None, path: str, query: str, fragment: str, raw: str) -> None:
        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment
        self.raw = raw

    @classmethod
    def parse(cls, uri: str) -> "URI":
        parser = URIParser(uri)
        return parser.parse()
    
    @classmethod
    def safe_parse(cls, uri: str) -> "URI":
        result = urlparse(uri)
        return cls(
            result.scheme,
            URIAuthority(
                URIUserInfo(
                    result.username,
                    result.password,
                ) if result.username or result.password else None,
                result.hostname,
                result.port
            ) if result.netloc else None,
            result.path,
            result.params,
            result.fragment,
            uri
        )
