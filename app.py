import io
import os
import streamlit as st
st.title("Crossword Generator")
max_grid_size = st.number_input("Max grid size", value=30)
n_variants = st.number_input("Number of variants", value=120)
pdf_title = st.text_input("PDF title", value="CST Theory Crossword")
pdf_instruction = st.text_input("PDF instruction", value="Use your CST notes and ChatGPT if needed.")
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