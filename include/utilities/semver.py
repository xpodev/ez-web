import re

from pydantic import BaseModel, model_validator, model_serializer

SEMVER_UNTIL_MAJOR = "^"
SEMVER_UNTIL_MINOR = "~"
SEMVER_GREATER = ">"
SEMVER_GREATER_EQUAL = ">="
SEMVER_LESS = "<"
SEMVER_LESS_EQUAL = "<="

SEMVER_ANY = "*"
SEMVER_LATEST = "latest"

SEMVER_REGEX_STRING = r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
SEMVER_OPTIONS_REGEX_STRING = r"(?P<option>(?:\^|~|>|>=|<|<=))?"
SEMVER_REGEX = re.compile(f"^({SEMVER_OPTIONS_REGEX_STRING})?{SEMVER_REGEX_STRING}$")


class SemanticVersion(BaseModel):
    major: int
    minor: int
    patch: int
    pre_release: str = ""
    build: str = ""

    option: str | None = None

    @property
    def is_latest(self):
        return self.major == -1
    
    @property
    def is_any(self):
        return self.major == 0 and self.minor == 0 and self.patch == 0
    
    def is_compatible(self, required: "SemanticVersion"):
        if required.is_any:
            return True
        
        if required.is_latest:
            raise ValueError("Cannot compare with latest version")
        if self.is_any:
            raise TypeError("Current version cannot be any")
        if self.is_latest:
            raise TypeError("Current version cannot be latest")
        if self.option:
            raise TypeError("Cannot compare with version range")
        
        if not required.option:
            return self == required
        if required.option == SEMVER_UNTIL_MAJOR:
            return self.major == required.major and self >= required
        if required.option == SEMVER_UNTIL_MINOR:
            return self.major == required.major and self.minor == required.minor and self.patch >= required.patch
        if required.option == SEMVER_GREATER:
            return self > required
        if required.option == SEMVER_GREATER_EQUAL:
            return self >= required
        if required.option == SEMVER_LESS:
            return self < required
        if required.option == SEMVER_LESS_EQUAL:
            return self <= required
        return False

    @classmethod
    def parse(cls, version: str):
        return cls.model_validate(cls.parse_json(version))
    
    @classmethod
    def parse_json(cls, version: str):
        if version == SEMVER_ANY:
            return {
                "major": 0,
                "minor": 0,
                "patch": 0,
                "pre_release": "",
                "build": ""
            }
        if version == SEMVER_LATEST:
            return {
                "major": -1,
                "minor": 0,
                "patch": 0,
                "pre_release": "",
                "build": "latest"
            }
        
        match = SEMVER_REGEX.match(version)
        if not match:
            raise ValueError(f"Invalid semantic version: {version}")
        
        option = match.group("option")
        major = int(match.group("major"))
        minor = int(match.group("minor"))
        patch = int(match.group("patch"))
        pre_release = match.group("prerelease") or ""
        build = match.group("buildmetadata") or ""

        return {
            "major": major,
            "minor": minor,
            "patch": patch,
            "pre_release": pre_release,
            "build": build,
            "option": option
        }

    # @root_validator(pre=True)
    @model_validator(mode="before")
    @classmethod
    def _model_parse(cls, data):
        if isinstance(data, str):
            return cls.parse_json(data)
        return data
    
    @model_serializer
    def _model_serialize(self):
        return str(self)
    
    def __str__(self):
        if self.is_any:
            return SEMVER_ANY
        if self.is_latest:
            return SEMVER_LATEST
        return f"{self.major}.{self.minor}.{self.patch}{f'-{self.pre_release}' if self.pre_release else ''}{f'+{self.build}' if self.build else ''}"
    
    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch and self.pre_release == other.pre_release and self.build == other.build
    
    def __lt__(self, other):
        if self.major < other.major:
            return True
        if self.major > other.major:
            return False
        if self.minor < other.minor:
            return True
        if self.minor > other.minor:
            return False
        if self.patch < other.patch:
            return True
        if self.patch > other.patch:
            return False
        if self.pre_release and not other.pre_release:
            return True
        if not self.pre_release and other.pre_release:
            return False
        if self.pre_release < other.pre_release:
            return True
        if self.pre_release > other.pre_release:
            return False
        return False
    
    def __le__(self, other):
        return self == other or self < other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}{f'-{self.pre_release}' if self.pre_release else ''}{f'+{self.build}' if self.build else ''}"
