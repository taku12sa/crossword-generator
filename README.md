# Crossword Generator

A tool for teachers to generate printable crossword worksheet PDFs from a CSV file.

## Why this tool?

Crosswords are effective for vocabulary learning, but most generators create only one puzzle, making it easy for students to copy answers.

This tool generates multiple variants from a single word list, allowing teachers to distribute different puzzles and reduce copying.

## Example output

![Example crossword](screenshot.png)

## Try it

Try it online at https://crossword-generator-n55sxjze3pohsrt5yy2olp.streamlit.app/

## How to use

1. Download the CSV template: [sample.csv](sample.csv)
2. Open it in Excel (or similar)
3. Fill in words and definitions
4. Upload the CSV file to the app
5. Set parameters if needed
6. Click "Generate"
7. Download the PDF

## CSV format

Each row:

word,definition

Example:

dot, An extension is the part of a filename after this.<br>
pptx, The file extension for a MS PowerPoint file.

## Notes

* Large values of "Number of variants" may take longer to generate
* If generation is slow, reduce the number of variants