# Crossword Generator

A tool for teachers to generate printable crossword worksheet PDFs from a TSV or CSV file of words and definitions.

## Why this tool?

Crosswords are effective for vocabulary learning, but most generators create only one puzzle, making it easy for students to copy answers.

This tool generates multiple variants from a single word list, allowing teachers to distribute different puzzles and reduce copying.

## Example output

![Example crossword](screenshot.png)

## Try it for free

Try it online at https://crossword-generator-n55sxjze3pohsrt5yy2olp.streamlit.app/

## How to use

1. Download the TSV template: [sample.tsv](sample.tsv)
2. Open it in Excel (or similar)
3. Fill in words and definitions
4. Upload the TSV file to the app (CSV files are also supported)
5. Set parameters if needed
6. Click "Generate"
7. Download the PDF

## Theme color

Choose a theme color from the preset color list before generating the worksheet. To use a different color, open `Advanced: Custom color` and select any RGB color with the color picker. The default theme preserves the original blue color scheme.

## TSV format

Each row contains a word and its definition, separated by a tab. TSV is recommended because definitions can contain commas without additional quoting.

Example:

word\tdefinition

dot\tAn extension is the part of a filename after this.<br>
pptx\tThe file extension for a MS PowerPoint file.

CSV files are also supported. In CSV files, separate the word and definition with a comma and quote fields when needed.

## Notes

* Large values of "Number of variants" may take longer to generate
* If generation is slow, reduce the number of variants

## Run locally (optional)

Only needed if you want to run the app on your own machine.
You can ignore this section if you are using the online version.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The application entry point is `app.py`, which loads TSV or CSV input, generates crossword variants, and writes the result as a PDF.