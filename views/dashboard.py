import streamlit as st

import sqlite3
from backend.database import crear_tablas
from backend.pacientes import registrar_paciente

crear_tablas()


def mostrar_dashboard() -> None:
    """Muestra las vistas disponibles después del inicio de sesión."""
    st.title("Sistema de Gestión de Citas")
    st.success(
        f"Bienvenido, {st.session_state.get('usuario_actual', 'usuario')}."
    )

    opcion = st.sidebar.radio(
        "Menú principal",
        ["Inicio", "Pacientes", "Gestión de citas"],
    )

    if opcion == "Inicio":
        st.header("Panel principal")
        st.write("Bienvenido al Sistema de Gestión de Citas.")
    elif opcion == "Pacientes":
        mostrar_pacientes()
    else:
        st.header("Gestión de citas")
        st.info("Aquí programaremos las citas.")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.sesion_iniciada = False
        st.session_state.pop("usuario_actual", None)
        st.rerun()


def mostrar_pacientes() -> None:
    """Muestra el formulario para registrar pacientes."""
    st.header("Gestión de pacientes")
    st.subheader("Registro de pacientes")
    

    with st.form("formulario_pacientes"):
        nombre = st.text_input("Nombre completo")
        documento = st.text_input("Número de documento")
        edad = st.number_input("Edad", min_value=0, max_value=120)
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo electrónico")
        guardar = st.form_submit_button("Registrar paciente")

        if guardar:
            if nombre.strip() and documento.strip():
                try:
                    registrar_paciente(
                        nombre.strip(),
                        documento.strip(),
                        edad,
                        telefono.strip(),
                        correo.strip()
                    )
                    st.success("Paciente guardado en la base de datos.")
                except sqlite3.IntegrityError:
                    st.error("Ya existe un paciente con ese documento.")
            else:
                st.error("Debe ingresar el nombre y el documento.")
