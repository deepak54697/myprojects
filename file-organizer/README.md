# File Organizer

A Python CLI that sorts a folder's immediate files into categories such as Documents, Images and Spreadsheets. It previews changes first and never replaces an existing destination file.

Personal portfolio project for **Deepak Puligilla**, developed with AI assistance. No third-party packages; Python 3.10+.

## Try the sample safely

From this project folder, create a disposable copy of the sample inbox:

```bash
python -c "import shutil; shutil.copytree('examples/inbox', 'demo-inbox')"
python organizer.py demo-inbox
python organizer.py demo-inbox --apply
python -m unittest discover -s tests -v
```

Use `py` on Windows or `python3` on Linux/macOS if needed. The copy command expects `demo-inbox` not to exist. Preview creates no folders and moves no files. Apply sorts the three fictional sample files:

| Before | After |
| --- | --- |
| notes.txt | Documents/notes.txt |
| stock.csv | Spreadsheets/stock.csv |
| settings.json | Code/settings.json |

## How the code works

1. `argparse` reads the folder argument and optional `--apply` switch.
2. `Path.iterdir()` reads immediate directory entries. Hidden files, symlinks and subfolders are skipped.
3. `category_for()` compares each file's lowercase suffix with sets of known extensions. Unknown extensions use Other.
4. `organize()` checks the destination. An existing file is a conflict; a symlink or file in place of a category folder blocks the operation. Files occupying reserved category names are left for manual renaming.
5. Preview returns planned changes. Apply creates a category folder, creates an exclusive hard link and removes the original directory entry.
6. The CLI prints each result. Exit code 0 means no conflicts/errors; 1 means at least one item needs attention; 2 means invalid input or a folder access error.

## Why hard links?

Creating a hard link fails if the destination exists, protecting against overwriting during a competing destination creation. Both directory entries temporarily reference the same file data, then the old name is removed. This requires same-volume hard-link support (for example NTFS or a normal Linux filesystem). Unsupported drives return an error and retain the original. This is not a copy to another disk.

If removal of the original name fails, both names remain and the tool reports `partial`; inspect them manually. The operation is per-file, not a transaction across the folder. Category folder creation can remain after a failed move.

## Scope

Use a disposable folder first. Do not modify files or category directories concurrently while the program is running. It does not provide undo, recursive organization, content analysis or support for actively changing folders. It is not hardened against another process replacing category paths mid-operation. A name conflict is skipped rather than renamed.

## Skills demonstrated

Filesystem automation, command-line arguments, sets and dictionaries, exception handling, non-destructive previews and temporary-directory testing.

## Learn it / interview practice

Explain why `.PNG` matches `.png`, why preview returns before moving, and how name conflicts are handled. Your first extension: add an Ebooks category with `.epub`, then add a test. Run and understand this AI-assisted project before presenting implementation experience.
