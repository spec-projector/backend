import json
import pathlib
from typing import IO, Dict, List, Optional

from tests.helpers.path_finder import find_path

ASSETS_FOLDER = "assets"


class AssetsProvider:
    """Assets provider."""

    def __init__(self, fspath) -> None:
        """Init provider."""
        self._cwd: pathlib.Path = pathlib.Path(fspath)
        self._opened_files: List[object] = []

    def open_file(
        self,
        filename: str,
        mode: str = "rb",
        encoding: Optional[str] = None,
    ) -> IO[str]:
        """Open file and return a stream."""
        filepath = find_path(self._cwd, filename)

        file_handler = open(filepath, mode, encoding=encoding)  # noqa: WPS515
        self._opened_files.append(file_handler)
        return file_handler

    def read_json(self, filename: str) -> Dict[str, object]:
        """Read json file to dict."""
        return json.loads(
            self.open_file(
                "{0}.json".format(filename),
                mode="r",
            ).read(),
        )

    def close(self) -> None:
        """Close opened files."""
        for file_handler in self._opened_files:
            if not file_handler.closed:  # type: ignore
                file_handler.close()  # type: ignore
        self._opened_files.clear()
