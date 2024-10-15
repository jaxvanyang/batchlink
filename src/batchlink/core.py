"""Module providing batchlink core APIs."""

import re
import shutil
import sys
from os import PathLike
from pathlib import Path


def formatted_paths(paths: list[Path], template: str) -> list[Path]:
    """Format paths using the template.

    Args:
        paths: A list of file paths.
        template: A format string. The following variables can be used in it for
          replacement:
            - i: int, the zero-based number.
            - num: int, the one-based number.
            - path: Path, the original file path.
            - name: str, the final path component (i.e. path.name), excluding the drive
              and root, if any.
            - suffix: str, the file extension of the final component (i.e. path.suffix),
              if any.
            - suffixes: str, the overall file extension of the final component (i.e.
              ''.join(path.suffixes)).
            - stem: str, the final path component (i.e. path.stem), without its suffix.

    Returns:
        A new list of formatted paths.
    """

    new_paths = []
    for i, path in enumerate(paths):
        new_paths.append(
            Path(
                template.format(
                    i=i,
                    num=i + 1,
                    path=path,
                    name=path.name,
                    suffix=path.suffix,
                    suffixes="".join(path.suffixes),
                    stem=path.stem,
                )
            )
        )

    return new_paths


def pretty_print(*strs, sep=" ", end="\n", file=None, flush=False) -> None:
    """Print colored text of objects to the text stream file if it's interactive.

    If the file is not interactive, ANSI escape codes are removed from formatted
    strings.

    Args:
        *strs: The format strings to be printed, which may contain the replacement
          fields - black, red, green, yellow, blue, magenta, cyan, white and reset. For
          example, '{green}hello{reset} {red}world{reset}'.
        sep: String inserted between values. Default is a space.
        end: String appended after the last value. Default is a newline.
        file: A file-like object (stream). Default is the current sys.stdout.
        flush: Whether to forcibly flush the stream.
    """

    if file is None:
        file = sys.stdout

    color_dict = {
        "black": "\x1b[30m",
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
        "white": "\x1b[37m",
        "reset": "\x1b[m",
    }

    strs = [s.format(**color_dict) for s in strs]

    if not file.isatty():
        escape = re.compile(r"\x1b\[(\d|;)*m", re.ASCII)
        strs = [re.sub(escape, "", s) for s in strs]

    print(*strs, sep=sep, end=end, file=file, flush=flush)


def add_underline(text: str) -> str:
    """Add underline to the text."""

    return f"\x1b[4m{text}\x1b[m"


def _highlight_numbers(path: PathLike) -> str:
    """Return a string representation of the path with highlighted numbers."""

    numbers = re.compile(r"(\d+)")

    return re.sub(numbers, "\x1b[4;32m\\1\x1b[m", str(path))


def remove(path: PathLike, *, dry_run: bool = False, file=None) -> None:
    """Remove the file, symbolic link or directory of the path, if exists.

    This function also print a message to the file before removing.

    Args:
        path: The path of file to be removed.
        file: The file-like object (stream) to print message to. Default is the current
          sys.stdout.
    """

    if file is None:
        file = sys.stdout

    if not isinstance(path, Path):
        path = Path(path)

    path_text = add_underline(_highlight_numbers(path))

    if path.is_dir() or path.is_file():
        pretty_print(f"{{yellow}}Remove{{reset}} {path_text}", file=file)

    if dry_run:
        return

    if path.is_dir():
        path.rmdir()
    elif path.is_file():
        path.unlink()


def batch_link(
    src_paths: list[Path],
    dest_paths: list[Path],
    *,
    src: Path | None = None,
    dest: Path | None = None,
    symbolic: bool = False,
    relative: bool = False,
    rename: bool = False,
    copy: bool = False,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    """Batch link or rename files.

    Create links under the destination directory to corresponding files under the source
    directory by default.

    Args:
        src_paths: A list of file paths to be linked to (or renamed from).
        dest_paths: A list of file paths to be linked (or renamed to).
        src: The source directory which contains source files. Default is the current
          working directory.
        dest: The destination directory which contains target links (or files). Default
          is the current working directory.
        symbolic: If True create symbolic links instead of hard links.
        relative: If True create relative symbolic links instead of absolute symbolic
          links.
        rename: If True rename files instead of creating links.
        copy: If True copy files instead of creating links. This argument has
          higher priority than rename.
        force: If True remove existing destination files.
        dry_run: If True only show actions to be taken without creating links or
          renaming files.

    Raises:
        ValueError: One of the given argument is invalid.
    """

    if src is None:
        src = Path()
    if dest is None:
        dest = Path()

    if len(src_paths) != len(dest_paths):
        raise ValueError("the size of src_paths and dest_paths is not equal")

    if len(dest_paths) != len(set(dest_paths)):
        raise ValueError("dest_paths has repeated paths")

    def rename_file(src_path: Path, dest_path: Path):
        src_path_text = add_underline(_highlight_numbers(src_path))
        dest_path_text = add_underline(_highlight_numbers(dest_path))

        if force:
            remove(dest_path, dry_run=dry_run)

        pretty_print(f"{{blue}}Rename{{reset}} {src_path_text} -> {dest_path_text}")

        if dry_run:
            return

        src_path.rename(dest_path)

    def copy_file(src_path: Path, dest_path: Path):
        src_path_text = add_underline(_highlight_numbers(src_path))
        dest_path_text = add_underline(_highlight_numbers(dest_path))

        if force:
            remove(dest_path, dry_run=dry_run)

        pretty_print(f"{{blue}}Copy{{reset}} {src_path_text} -> {dest_path_text}")

        if dry_run:
            return

        if src_path.is_file():
            shutil.copy(src_path, dest_path)
        else:
            shutil.copytree(src_path, dest_path)

    def link_file(src_path: Path, dest_path: Path):
        link_type = "symbolic" if symbolic else "hard"
        if symbolic:
            if sys.version_info[0] != 3 or sys.version_info[1] < 12:
                raise ValueError(
                    "batchlink only support creating relative symbolic links with "
                    "Python 3.12+ for now"
                )

            src_path = (
                src_path.relative_to(dest_path.parent, walk_up=True)
                if relative
                else src_path.resolve()
            )

        src_path_text = add_underline(_highlight_numbers(src_path))
        dest_path_text = add_underline(_highlight_numbers(dest_path))

        if force:
            remove(dest_path, dry_run=dry_run)

        pretty_print(
            f"{{blue}}Create {link_type} link{{reset}} {dest_path_text} -> "
            f"{src_path_text}"
        )

        if dry_run:
            return

        if symbolic:
            dest_path.symlink_to(src_path)
        else:
            dest_path.hardlink_to(src_path)

    for src_path, dest_path in zip(src_paths, dest_paths):
        src_path = src / src_path
        dest_path = dest / dest_path

        if copy:
            copy_file(src_path, dest_path)
        elif rename:
            rename_file(src_path, dest_path)
        else:
            link_file(src_path, dest_path)
