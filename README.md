# Combine Files

Combine Files is a Python script that aggregates text files from a specified directory into a single output document. This tool is particularly useful for developers who need to compile all relevant code into a single document for review, debugging, or sharing purposes, especially when working with AI-powered coding assistants.

## Features

- Combines text files from the current directory and its subdirectories into a single document.
- Intelligently detects and excludes virtual environment directories.
- Allows for custom exclusion patterns and virtual environment names.
- Provides a progress bar and colored output for better user experience.
- Copies the output to the clipboard (with size warning and user confirmation).
- Adds a list of included files at the end of the output document.
- Excludes common non-text files and directories.

## Installation

1. Clone the repository or download the source code:

   ```
   git clone https://github.com/yourusername/combine-files.git
   cd combine-files
   ```

2. Ensure you have Python 3.6 or later installed on your system.
3. No additional dependencies are required as the script uses only Python standard library modules.

## Usage

Run the script from the command line:

```
python combine_files.py [OPTIONS]
```

Options:
- `--exclude`: Comma-separated patterns to exclude from the search.
- `--include`: Space-delimited file names to explicitly include in the output.
- `--output`: Name of the output file (default: output_document.txt).
- `--verbose`: Enable verbose output.
- `--clipboard`: Copy output to clipboard (with size warning).
- `--custom-venv`: Comma-separated custom virtual environment folder names to exclude.

Example:

```
python combine_files.py --clipboard --verbose --custom-venv myenv,customenv
```

## Advanced Setup

### Creating an Alias (for bash shell users on Mac)

To create an alias that allows you to invoke the script by typing a single command, follow these steps:

1. Open your `.bash_profile` file in a text editor:
   ```
   nano ~/.bash_profile
   ```

2. Add the following line to the file (replace `/path/to/combine_files.py` with the actual path to your script):
   ```
   alias combine_files='python /path/to/combine_files.py'
   ```

3. Save the file and exit the text editor (in nano, press Ctrl+X, then Y, then Enter).

4. Reload your `.bash_profile`:
   ```
   source ~/.bash_profile
   ```

Now you can run the script by simply typing `combine_files` in your terminal.

### Creating a Binary Version (for Mac users)

To create a standalone binary version of the script, you can use PyInstaller. Here's how:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Navigate to the directory containing your script:
   ```
   cd /path/to/script/directory
   ```

3. Create the binary:
   ```
   pyinstaller --onefile combine_files.py
   ```

4. The binary will be created in the `dist` directory. You can move it to a location in your PATH for easy access:
   ```
   sudo mv dist/combine_files /usr/local/bin/
   ```

Now you can run the script by typing `combine_files` in your terminal from any directory.

## The Story Behind Combine Files

This script was created to streamline the process of sharing code context with AI-powered coding assistants. When working on large projects, it's often necessary to provide substantial code context to get accurate and relevant assistance. However, copying and pasting multiple files or large code sections can be time-consuming and error-prone.

Combine Files automates this process by aggregating all relevant text files into a single document, making it easy to share comprehensive code context with AI assistants or human collaborators. The script intelligently excludes non-text files, virtual environments, and other unnecessary data, ensuring that only the relevant code is included in the output.

## File Structure

- `combine_files.py`: The main Python script containing all the logic for combining files.
- `README.md`: This file, providing information about the project.

## Dependencies

This script uses only Python standard library modules, ensuring easy portability and minimal setup requirements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please contact ashakoen@gmail.com.