import os

def see_file_tree(path: str = ".") -> list[str]:
    """Returns a list of relative paths for all files and directories starting from path."""
    tree = []

    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in {".git", ".venv", "__pycache__", ".ipynb_checkpoints"}]

        for name in sorted(dirnames + filenames):
            full_path = os.path.join(dirpath, name)
            tree.append(os.path.relpath(full_path, path))

    return tree


if __name__ == "__main__":
    import sys

    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    for item in see_file_tree(target_path):
        print(item)