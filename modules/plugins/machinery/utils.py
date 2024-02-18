from pathlib import Path


class InstallerHelper:
    def __init__(self, root: str) -> None:
        self._files: list[str] = []
        self.root = Path(root)

    def add_file(self, file: str):
        self._files.append(file)

    def _move_file(self, src: str, dest: str, name: str = None, exclude: bool = False):
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        src = Path(src)
        src.rename(dest / (name or src.name))
        if not exclude:
            self.add_file(str(dest / (name or src.name)))


    def install_file(self, src: str, dest: str, name: str = None, exclude: bool = False):
        self._move_file(src, dest, name, exclude=exclude)

    def install_dir(self, src: str, dest: str, exclude: bool = False):
        src = Path(src)
        dest = Path(dest)
        for file in src.iterdir():
            if file.is_dir(): 
                self.install_dir(file, dest / file.name, exclude)
            else:
                self._move_file(file, dest, exclude=exclude)

    def finalize(self, uninstallation_filename: str):
        with open(self.root / uninstallation_filename, "w") as file:
            for f in self._files:
                file.write(f"{f}\n")
