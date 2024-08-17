import sys
import argparse
from pathlib import Path
from typing import List, Optional, Set
import subprocess
import mimetypes

def print_color(text: str, color: str = 'default'):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'default': '\033[0m',
    }
    print(f"{colors.get(color, colors['default'])}{text}{colors['default']}")

def progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 50, fill: str = '█', print_end: str = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total: 
        print()

def is_text_file(filepath: Path) -> bool:
    mime_type, _ = mimetypes.guess_type(str(filepath))
    if mime_type and mime_type.startswith('text'):
        return True
    
    text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.log', '.ini', '.cfg', '.yml', '.yaml', '.swift'}
    if filepath.suffix.lower() in text_extensions:
        return True
    
    try:
        with filepath.open('r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False

def is_venv_directory(path: Path, custom_venv_names: Set[str]) -> bool:
    common_venv_names = {'venv', 'env', '.env', 'virtualenv', '.venv', 'myenv'}
    common_venv_names.update(custom_venv_names)
    
    if path.name.lower() in common_venv_names:
        return True
    
    venv_indicators = [
        'bin/activate',
        'Scripts/activate.bat',
        'pyvenv.cfg',
        'lib/python',
        'Include',
        'Lib/site-packages'
    ]
    return any((path / indicator).exists() for indicator in venv_indicators)

def should_exclude(file: Path, excluded_extensions: Set[str], excluded_dirs: Set[str], custom_venv_names: Set[str]) -> bool:
    if file.name.startswith('.') or file.name == '.DS_Store':
        return True
    if file.suffix.lower() in excluded_extensions:
        return True
    if any(part in excluded_dirs for part in file.parts):
        return True
    if any(is_venv_directory(file.parent, custom_venv_names) for _ in file.parts):
        return True
    return False

def check_and_confirm_clipboard(file_path: Path, threshold_kb: float = 500) -> bool:
    file_size_kb = file_path.stat().st_size / 1024
    if file_size_kb > threshold_kb:
        print_color(f"Warning: The output file is {file_size_kb:.2f} KB.", 'yellow')
        print_color(f"Copying large amounts of text to the clipboard may affect system performance.", 'yellow')
        user_input = input("Do you still want to copy the content to clipboard? (y/n): ").lower()
        return user_input == 'y'
    return True

def copy_to_clipboard(text: str):
    if sys.platform == 'darwin':  # macOS
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
    elif sys.platform == 'win32':  # Windows
        subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
    else:  # Linux and other platforms
        try:
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        except FileNotFoundError:
            print_color("xclip not found. Unable to copy to clipboard.", 'yellow')

def combine_files(exclude_patterns: List[str], include_files: Optional[List[str]], output_file: str, verbose: bool, copy_clipboard: bool, custom_venv_names: Set[str], dry_run: bool):
    base_dir = Path.cwd()

    excluded_dirs = {
        'node_modules', '.git', 'build', 'dist', '__pycache__',
        '.idea', '.vscode', 'assets', 'images', 'logs', 'temp', '.tmp'
    }

    excluded_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg',
        '.mp3', '.wav', '.mp4', '.avi', '.mov', '.mkv', '.pdf', '.zip',
        '.tar', '.gz', '.7z', '.rar', '.ttf', '.woff', '.woff2', '.eot',
        '.bin', '.pickle', '.pyc', '.pyo', '.pyd', '.dll', '.so', '.dylib',
        '.exe', '.bat', '.cmd', '.o', '.obj', '.a', '.lib', '.exp',
        '.db', '.sqlite', '.sqlitedb', '.mdf', '.ldf',
        '.class', '.jar', '.war', '.ear',
        '.pkl', '.npy', '.npz', '.mat', '.fits',
        '.mod', '.testcase'
    }

    output_content = ""
    included_files = []

    print_color("Analyzing files..." if dry_run else "Combining files...", 'cyan')
    if verbose:
        print_color(f"Custom venv names to exclude: {custom_venv_names}", 'yellow')
        print_color(f"Files to include: {include_files}", 'cyan')

    files_to_process = []
    if include_files:
        for file in include_files:
            file_path = Path(file)
            if not file_path.is_absolute():
                file_path = base_dir / file_path
            if file_path.is_file():
                files_to_process.append(file_path)
            elif file_path.is_dir():
                files_to_process.extend(file_path.rglob('*'))
            else:
                print_color(f"Warning: File or directory not found: {file_path}", 'yellow')
    else:
        files_to_process = list(base_dir.rglob('*'))

    total_files = len(files_to_process)
    processed_files = 0

    for filepath in files_to_process:
        if filepath.is_file():
            processed_files += 1
            progress_bar(processed_files, total_files, prefix='Progress:', suffix='Complete', length=50)
            
            if should_exclude(filepath, excluded_extensions, excluded_dirs, custom_venv_names):
                if verbose:
                    print_color(f"Excluding file: {filepath}", 'yellow')
                continue

            if any(pattern in filepath.name for pattern in exclude_patterns):
                if verbose:
                    print_color(f"Excluding file: {filepath}", 'yellow')
                continue

            if not is_text_file(filepath):
                if verbose:
                    print_color(f"Skipping non-text file: {filepath}", 'yellow')
                continue

            included_files.append(str(filepath.relative_to(base_dir)))
            if verbose:
                print_color(f"{'Would include' if dry_run else 'Including'} file: {filepath}", 'green')

            if not dry_run:
                try:
                    with filepath.open('r', encoding='utf-8') as infile:
                        file_content = f"##{filepath.relative_to(base_dir)}\n\n{infile.read()}\n\n"
                        output_content += file_content
                except UnicodeDecodeError:
                    print_color(f"Skipping file due to encoding issues: {filepath}", 'red')

    # Add the list of included files at the end
    file_list = "\n## Files Included Above\n\n"
    for file in included_files:
        file_list += f"- {file}\n"
    output_content += file_list

    if dry_run:
        print_color("\nDry run completed. No files were combined.", 'green')
        print_color(f"Total files that would be included: {len(included_files)}", 'green')
        print_color("Files that would be included:", 'cyan')
        for file in included_files:
            print_color(f"- {file}", 'default')
    else:
        output_file_path = Path(output_file)
        with output_file_path.open('w', encoding='utf-8') as outfile:
            outfile.write(output_content)
        print_color(f"\nOutput written to {output_file}", 'green')
        print_color(f"Total files included: {len(included_files)}", 'green')

        if copy_clipboard:
            if check_and_confirm_clipboard(output_file_path):
                copy_to_clipboard(output_content)
                print_color("Output copied to clipboard", 'green')
            else:
                print_color("Clipboard copy cancelled by user", 'yellow')

def main():
    parser = argparse.ArgumentParser(description="Combine multiple text files into a single document.")
    parser.add_argument('--exclude', default="", help='Comma-separated patterns to exclude from the search.')
    parser.add_argument('--include', nargs='+', help='File or directory names to explicitly include in the output. Names with spaces are automatically handled.')
    parser.add_argument('--output', default="output_document.txt", help='Name of the output file.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('--clipboard', action='store_true', help='Copy output to clipboard.')
    parser.add_argument('--custom-venv', default="", help='Comma-separated custom virtual environment folder names to exclude.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without creating the output file.')

    args = parser.parse_args()

    exclude_patterns = args.exclude.split(',') if args.exclude else []
    include_files = args.include if args.include else None
    custom_venv_names = set(name.strip().lower() for name in args.custom_venv.split(',') if name.strip())
    
    combine_files(exclude_patterns, include_files, args.output, args.verbose, args.clipboard, custom_venv_names, args.dry_run)

if __name__ == '__main__':
    main()