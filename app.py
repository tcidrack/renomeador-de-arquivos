import os
import zipfile
from io import BytesIO
import streamlit as st

def validate_login():
    """Valida usuário e senha usando st.secrets."""
    username = st.session_state.username
    password = st.session_state.password
    if username in users and password == users[username]:
        st.session_state.logged_in = True
        st.success(f"✅ Bem-vindo(a), {username}!")
    else:
        st.session_state.logged_in = False
        st.error("Usuário ou senha incorretos!")

def rename_file(file_name):
    """
    Renomeia arquivo adicionando '_faturamento_auditoria' ao final.
    Mantém apenas a parte numérica do nome como base, se houver.
    """
    file_base, file_ext = os.path.splitext(file_name)
    numeric_part = ''.join(c for c in file_base if c.isdigit())
    if file_base.endswith("_faturamento_auditoria"):
        base_name = numeric_part if numeric_part else file_base.replace("_faturamento_auditoria", "")
    else:
        base_name = numeric_part if numeric_part else file_base
    return base_name + "_faturamento_auditoria" + file_ext

st.set_page_config(page_title="Renomeador de Arquivos", layout="centered")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("📄 Renomeador de Arquivos - Faturamento Auditoria")
st.write("Envie seus arquivos e eles serão renomeados automaticamente com o sufixo **_faturamento_auditoria**.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = st.secrets["app"]["users"]

if not st.session_state.logged_in:
    with st.form("login_form"):
        st.text_input("Usuário", key="username")
        st.text_input("Senha", key="password", type="password")
        submit = st.form_submit_button("Entrar")
        if submit:
            validate_login()

if st.session_state.logged_in:
    uploaded_files = st.file_uploader(
        "Selecione ou arraste seus arquivos aqui",
        accept_multiple_files=True
    )

    if uploaded_files:
        st.write(f"Arquivos selecionados ({len(uploaded_files)}):")
        for file in uploaded_files:
            st.write(f"- {file.name} ({round(len(file.getbuffer())/1024, 1)} KB)")

        output_buffer = BytesIO()
        with zipfile.ZipFile(output_buffer, "w") as zipf:
            for file in uploaded_files:
                new_name = rename_file(file.name)
                zipf.writestr(new_name, file.read())
                file.seek(0)

        output_buffer.seek(0)
        st.download_button(
            label="📥 Baixar arquivos renomeados (.zip)",
            data=output_buffer,
            file_name="arquivos_renomeados.zip",
            mime="application/zip"
        )
