import streamlit as st
import zipfile
from io import BytesIO
from pathlib import Path

st.set_page_config(page_title="Renomeador de Arquivos", layout="centered")
st.title("📄 Renomeador de Arquivos")

uploaded_files = st.file_uploader(
    "Selecione ou arraste seus arquivos aqui",
    accept_multiple_files=True,
    help="Você pode enviar vários arquivos de uma vez"
)

if uploaded_files:
    output_buffer = BytesIO()

    with zipfile.ZipFile(output_buffer, "w") as zipf:
        for file in uploaded_files:
            path = Path(file.name)
            file_name, file_ext = path.stem, path.suffix
            numeric_part = "".join(c for c in file_name if c.isdigit())

            if file_name.endswith("_faturamento_auditoria"):
                base_name = numeric_part if numeric_part else file_name.replace("_faturamento_auditoria", "")
            else:
                base_name = numeric_part if numeric_part else file_name

            new_name = base_name + "_faturamento_auditoria" + file_ext
            zipf.writestr(new_name, file.read())

    output_buffer.seek(0)
    st.download_button(
        label="📥 Baixar arquivos renomeados (.zip)",
        data=output_buffer,
        file_name="arquivos_renomeados.zip",
        mime="application/zip"
    )
