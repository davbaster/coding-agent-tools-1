import os
from pathlib import Path

class ProjectTools:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def see_file_tree(self, root_dir: str = ".") -> list[str]:
        """List files and directories in the project.
        Args:
            root_dir: Directory to list relative to the project root.
        """
        abs_root = self.project_dir / root_dir
        tree = []

        for dirpath, dirnames, filenames in os.walk(abs_root):
            dirnames[:] = [d for d in dirnames if d not in {".git", ".venv", "__pycache__"}]

            for name in sorted(dirnames + filenames):
                full_path = os.path.join(dirpath, name)
                tree.append(os.path.relpath(full_path, self.project_dir))

        return tree

    def read_file(self, filepath: str) -> str:
        """Read the contents of a file relative to the project root.
        Args:
            filepath: Path to the file to read.
        """
        if 'uv.lock' in filepath:
            return "you're not allowed to read this file"

        abs_path = self.project_dir / filepath
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: file '{filepath}' not found."