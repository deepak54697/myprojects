"""Organize immediate files by extension; preview by default. Python 3.10+."""
import argparse
import os
from pathlib import Path

CATEGORIES = {
    'Images': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'},
    'Documents': {'.pdf', '.doc', '.docx', '.txt', '.md'},
    'Spreadsheets': {'.csv', '.xlsx', '.xls', '.tsv'},
    'Media': {'.mp3', '.wav', '.mp4', '.mov'},
    'Archives': {'.zip', '.tar', '.gz', '.7z'},
    'Code': {'.py', '.js', '.ts', '.html', '.css', '.json'},
}


def category_for(path):
    return next((name for name, extensions in CATEGORIES.items()
                 if path.suffix.lower() in extensions), 'Other')


def organize(folder, apply=False):
    folder = Path(folder).resolve(strict=True)
    if not folder.is_dir():
        raise ValueError('Choose a folder, not a file')
    results = []
    for source in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if source.is_symlink() or not source.is_file() or source.name.startswith('.'):
            continue
        if source.name.casefold() in {name.casefold() for name in [*CATEGORIES, 'Other']}:
            results.append({'file': source.name, 'destination': '-', 'status': 'blocked',
                            'detail': 'File occupies a reserved category name; rename it manually'})
            continue
        category = folder / category_for(source)
        destination = category / source.name
        result = {'file': source.name, 'destination': str(destination.relative_to(folder))}
        if category.is_symlink() or (category.exists() and not category.is_dir()):
            result.update(status='blocked', detail='Category path is not a normal directory')
        elif destination.exists() or destination.is_symlink():
            result.update(status='conflict', detail='Existing destination was preserved')
        elif not apply:
            result['status'] = 'planned'
        else:
            try:
                category.mkdir(exist_ok=True)
                # A hard link creates the destination exclusively: no overwriting.
                # Removing the original directory entry completes a same-volume move.
                os.link(source, destination, follow_symlinks=False)
                try:
                    source.unlink()
                except OSError:
                    # Both names still point to the same data; report for manual review.
                    result.update(status='partial', detail='Destination created; original could not be removed')
                else:
                    result['status'] = 'moved'
            except FileExistsError:
                result.update(status='conflict', detail='Destination appeared during the operation')
            except OSError:
                result.update(status='error', detail='Move failed; check permissions and hard-link support')
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--apply', action='store_true', help='Move files; otherwise preview only')
    args = parser.parse_args()
    try:
        results = organize(args.folder, args.apply)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Cannot organize folder: {exc}\n')
    print('APPLY MODE' if args.apply else 'PREVIEW — no files changed')
    for row in results:
        print(f"{row['status']:8} {row['file']} -> {row['destination']}")
    print(f'{len(results)} file(s) examined')
    return int(any(row['status'] in {'error', 'partial', 'blocked', 'conflict'} for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
