import io
import os
import inspect
import streamlit as st
import main
import renderer


THEME_COLORS = {
    "#1f4e79": "Blue",
    "#2e75b6": "Light blue",
    "#548235": "Green",
    "#bf9000": "Gold",
    "#c55a11": "Orange",
    "#a61c00": "Red",
    "#7030a0": "Purple",
    "#666666": "Gray",
}


def hex_to_rgb(value):
    return tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))


st.title("Crossword Generator")
max_grid_size = st.number_input("Max grid size", value=30)
n_variants = st.number_input("Number of variants", value=120)
pdf_title = st.text_input("PDF title", value="CST Theory Crossword")
pdf_instruction = st.text_input("PDF instruction", value="Use your CST notes and ChatGPT if needed.")
theme_color_hex = st.radio(
    "Theme color",
    options=list(THEME_COLORS),
    format_func=THEME_COLORS.get,
    horizontal=True,
)
theme_color_hex = st.color_picker(
    "Selected theme color",
    value=theme_color_hex,
    help="Click the color swatch to adjust the selected theme color.",
)
uploaded_file = st.file_uploader("Upload CSV or TSV", type=["csv", "tsv"])
with st.expander("Debug info"):
    st.write("App file", __file__)
    st.write("Main file", main.__file__)
    st.write("Renderer file", renderer.__file__)
    st.write("Instruction layout", renderer.INSTRUCTION_LAYOUT_VERSION)
    st.write("pdf_writer signature", str(inspect.signature(main.pdf_writer)))
    if uploaded_file:
        st.write("Uploaded file", uploaded_file.name)
        st.write("Uploaded bytes", uploaded_file.size)
buffer = None

if uploaded_file and st.button("Generate"):
    extension = os.path.splitext(uploaded_file.name)[1].lower()
    if extension == ".csv":
        delimiter = ","
    elif extension == ".tsv":
        delimiter = "\t"
    else:
        st.error("Unsupported file type. Please upload a CSV or TSV file.")
        st.stop()

    buffer = io.BytesIO()
    print(
        f"Build={renderer.INSTRUCTION_LAYOUT_VERSION} "
        f"file={uploaded_file.name} bytes={uploaded_file.size} "
        f"instruction_length={len(pdf_instruction)}"
    )
    main.pdf_writer(
        pdf_title = pdf_title,
        pdf_instruction = pdf_instruction,
        infileobj = io.TextIOWrapper(uploaded_file, encoding="utf-8"),
        delimiter = delimiter,
        theme_color = hex_to_rgb(theme_color_hex),
        max_grid_size = max_grid_size,
        n_variants = n_variants,
    ).write(stream=buffer)

if buffer:
    st.download_button(
        "Download PDF",
        data = buffer.getvalue(),
        file_name = "crossword.pdf",
        mime = "application/pdf",
    )