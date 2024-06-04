"""Module providing batchlink core APIs."""

import shutil
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


def remove(file: PathLike, *, dry_run: bool = False) -> None:
    """Remove this file, symbolic link or directory, if exists.

    This function also print a message before removing.

    Args:
        file: The file to be removed.
    """

    if not isinstance(file, Path):
        file = Path(file)

    if file.is_dir() or file.is_file():
        print(f"\x1b[33mRemove\x1b[00m {file}")

    if dry_run:
        return

    if file.is_dir():
        file.rmdir()
    elif file.is_file():
        file.unlink()


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
        if force:
            remove(dest_path, dry_run=dry_run)

        print(f"\x1b[34mRename\x1b[00m {src_path} \x1b[34mto\x1b[00m {dest_path}")

        if dry_run:
            return

        src_path.rename(dest_path)

    def copy_file(src_path: Path, dest_path: Path):
        if force:
            remove(dest_path, dry_run=dry_run)

        print(f"\x1b[34mCopy\x1b[00m {src_path} \x1b[34mto\x1b[00m {dest_path}")

        if dry_run:
            return

        if src_path.is_file():
            shutil.copy(src_path, dest_path)
        else:
            shutil.copytree(src_path, dest_path)

    def link_file(src_path: Path, dest_path: Path):
        link_type = "symbolic" if symbolic else "hard"
        if symbolic:
            src_path = (
                src_path.relative_to(dest_path.parent, walk_up=True)
                if relative
                else src_path.resolve()
            )

        if force:
            remove(dest_path, dry_run=dry_run)

        print(
            f"\x1b[34mCreate {link_type} link\x1b[00m {dest_path} \x1b[34mto\x1b[00m "
            f"{src_path}"
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
