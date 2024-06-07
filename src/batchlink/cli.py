"""Module providing the batchlink CLI program."""

import sys
from argparse import ArgumentParser
from pathlib import Path

from batchlink import __version__, batch_link, formatted_paths


def make_parser() -> ArgumentParser:
    """Make CLI argument parser."""

    parser = ArgumentParser(
        "batchlink",
        description="Batch link files without modifying original files.",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version and exit.",
    )
    parser.add_argument(
        "-s",
        "--symbolic",
        action="store_true",
        help="Create symbolic links instead of hard links.",
    )
    parser.add_argument(
        "-r",
        "--rename",
        action="store_true",
        help="Rename files instead of linking.",
    )
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy files instead of linking. This option has higher priority than -r.",
    )
    parser.add_argument(
        "-R",
        "--relative",
        action="store_true",
        help="Create relative symbolic links instead of absolute symbolic links.",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Remove existing destination files."
    )
    parser.add_argument(
        "-S",
        "--src",
        default=Path(),
        type=Path,
        help="Set the source directory. Default is the current working directory.",
        metavar="directory",
    )
    parser.add_argument(
        "-d",
        "--dest",
        default=Path(),
        type=Path,
        help="Set the destination directory. Default is the current working directory.",
        metavar="directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't creat links or rename files. Only show actions to be taken.",
    )
    parser.add_argument(
        "input_pattern",
        help=(
            "Set the glob pattern of input file paths. This argument should be quoted "
            "File paths will be processed according to alphabetical order."
        ),
    )
    parser.add_argument(
        "output_template",
        help=(
            "Set the template of output link (or file) paths. The template is a Python "
            "format string. Available replacement fields are: i, num, path, name, "
            "suffix, suffixes, stem."
        ),
    )

    return parser


def main(args: list[str] | None = None) -> int:  # pylint: disable=C0116
    if args is None:
        args = sys.argv[1:]

    args = make_parser().parse_args(args)

    if not args.dest.is_dir():
        print(f"FileNotFoundError: [Erroro 2] No such directory: {args.dest}")
        return 2

    src_files = sorted(
        file.relative_to(args.src) for file in args.src.glob(args.input_pattern)
    )
    dest_files = formatted_paths(src_files, args.output_template)

    try:
        batch_link(
            src_files,
            dest_files,
            src=args.src,
            dest=args.dest,
            symbolic=args.symbolic,
            rename=args.rename,
            copy=args.copy,
            relative=args.relative,
            force=args.force,
            dry_run=args.dry_run,
        )
    except FileExistsError as e:
        print(e, file=sys.stderr)
        return e.errno
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
