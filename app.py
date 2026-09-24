import io
import os
import streamlit as st


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
with st.expander("Advanced: Custom color"):
    use_custom_color = st.checkbox("Use custom color")
    if use_custom_color:
        theme_color_hex = st.color_picker("Custom color", value=theme_color_hex)

st.markdown(
    f'<div style="display:flex;align-items:center;gap:0.5rem;">'
    f'<span style="display:inline-block;width:1.25rem;height:1.25rem;'
    f'border-radius:0.25rem;background:{theme_color_hex};'
    f'border:1px solid #888;"></span>'
    f'<span>Selected theme color: {THEME_COLORS.get(theme_color_hex, theme_color_hex)}</span>'
    f'</div>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader("Upload CSV or TSV", type=["csv", "tsv"])
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
    from main import pdf_writer
    pdf_writer(
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