import streamlit as st
import os
import zipfile
from io import BytesIO

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Renomeador de Arquivos", layout="centered")
st.title("📄 Renomeador de Arquivos")

# estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = st.secrets["app"]["users"]

# 🔑 só mostra o login se ainda não estiver logado
if not st.session_state.logged_in:
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login = st.form_submit_button("Entrar")

    if login:
        if username in users and password == users[username]:
            st.session_state.logged_in = True
            st.success(f"✅ Bem-vindo, {username}!")
            st.rerun()  # força atualizar a tela sem os campos
        else:
            st.error("Usuário ou senha incorretos!")

else:
    st.success("✅ Você já está logado!")

    # uploader aparece só depois do login
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
                numeric_part = ''.join(c for c in file_name if c.isdigit())

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
