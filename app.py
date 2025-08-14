import streamlit as st
import os
import zipfile
from io import BytesIO

# --- CSS para limpar menu e rodapé ---
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}  /* esconde menu hamburger */
    footer {visibility: hidden;}     /* esconde "Made with Streamlit" */
    </style>
    """,
    unsafe_allow_html=True
)

# --- Configurações do App ---
st.set_page_config(page_title="Renomeador de Arquivos", layout="centered")
st.title("📄 Renomeador de Arquivos - Faturamento Auditoria")
st.write("Envie seus arquivos e eles serão renomeados automaticamente com o sufixo **_faturamento_auditoria**.")

# --- Autenticação ---
senha_correta = st.secrets["app"]["senha"]
senha_digitada = st.text_input("Digite a senha para acessar:", type="password")
if senha_digitada != senha_correta:
    st.warning("Acesso restrito. Digite a senha correta.")
    st.stop()

st.success("✅ Acesso liberado!")

# --- Upload ---
uploaded_files = st.file_uploader(
    "Selecione ou arraste seus arquivos aqui",
    type=None,
    accept_multiple_files=True,
    help="Você pode enviar vários arquivos de uma vez"
)

if uploaded_files:
    output_buffer = BytesIO()

    with zipfile.ZipFile(output_buffer, "w") as zipf:
        for file in uploaded_files:
            file_name, file_ext = os.path.splitext(file.name)
            
            # Pega apenas os números do início
            numeric_part = ''.join(c for c in file_name if c.isdigit())

            # Garante que o sufixo não se duplique
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
