SCRIPT_NAME="combine_files.sh"  # Name of the script
OUTPUT_DOCUMENT="output_document.txt"  # Name of the output document
echo -e "\033[0;32mCombining files...\033[0m"
find . -type d \( -path "./venv" -o -path "./env" -o -path "./build" -o -path "./.git" \) -prune -o -type f ! -name "$SCRIPT_NAME" ! -name "$OUTPUT_DOCUMENT" -exec grep -Iq . {} \; -exec echo "Including: {}" \; -exec cat {} + > "$OUTPUT_DOCUMENT"
echo -e "\033[0;32mAppending file list...\033[0m"
echo -e "\nIncluded files:\n$(find . -type d \( -path "./venv" -o -path "./env" -o -path "./build" -o -path "./.git" \) -prune -o -type f ! -name "$SCRIPT_NAME" ! -name "$OUTPUT_DOCUMENT" -exec grep -Iq . {} \; -print)" >> "$OUTPUT_DOCUMENT"
if [[ $(wc -c <"$OUTPUT_DOCUMENT") -lt 1000000 ]]; then
    cat "$OUTPUT_DOCUMENT" | pbcopy
    echo -e "\033[0;32mOutput copied to clipboard.\033[0m"
else
    echo -e "\033[0;31mWarning: Output is too large to copy automatically.\033[0m"
fi
echo -e "\033[0;32mDone!\033[0m"