from pathlib import Path

import streamlit as st

from views.dashboard import mostrar_dashboard
from views.login import mostrar_login
from views.register import mostrar_registro


def cargar_estilos() -> None:
    """Carga los estilos comunes de la aplicación."""
    ruta_css = Path(__file__).parent / "styles" / "styles.css"
    st.markdown(
        f"<style>{ruta_css.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Sistema de Gestión de Citas",
    page_icon="📅",
    layout="centered",
)

cargar_estilos()

if "sesion_iniciada" not in st.session_state:
    st.session_state.sesion_iniciada = False

if "vista_publica" not in st.session_state:
    st.session_state.vista_publica = "login"

if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "admin": {
            "contrasena": "12345",
            "nombre": "Administrador",
        }
    }

if st.session_state.sesion_iniciada:
    mostrar_dashboard()
else:
    if st.session_state.vista_publica == "registro":
        mostrar_registro()
    else:
        mostrar_login()
