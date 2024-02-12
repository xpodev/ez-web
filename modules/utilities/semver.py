class SemanticVersion:
    major: int
    minor: int
    patch: int
    pre_release: str
    build: str

    def __init__(self, major: int, minor: int, patch: int, pre_release: str = "", build: str = ""):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre_release = pre_release
        self.build = build

    @classmethod
    def parse(cls, version: str):
        major, minor, patch = version.split(".")
        pre_release = ""
        build = ""

        if "-" in patch:
            patch, pre_release = patch.split("-")

        if "+" in pre_release:
            pre_release, build = pre_release.split("+")

        return cls(int(major), int(minor), int(patch), pre_release, build)
    
    def __str__(self):
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
    
    def is_compatible(self, other):
        return self.major == other.major and self.minor == other.minor
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}{f'-{self.pre_release}' if self.pre_release else ''}{f'+{self.build}' if self.build else ''}"
