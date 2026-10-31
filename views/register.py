import streamlit as st


def mostrar_registro() -> None:
    """Muestra la vista pública para registrar un usuario."""
    st.title("Sistema de Gestión de Citas")
    st.subheader("Crear una cuenta")

    with st.form("formulario_registro"):
        nombre = st.text_input("Nombre completo")
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        confirmar_contrasena = st.text_input(
            "Confirmar contraseña",
            type="password",
        )
        registrarse = st.form_submit_button("Registrarse")

    if registrarse:
        usuario_limpio = usuario.strip().lower()

        if not nombre.strip() or not usuario_limpio or not contrasena:
            st.error("Completa todos los campos.")
        elif usuario_limpio in st.session_state.usuarios:
            st.error("Ese usuario ya está registrado.")
        elif contrasena != confirmar_contrasena:
            st.error("Las contraseñas no coinciden.")
        else:
            st.session_state.usuarios[usuario_limpio] = {
                "contrasena": contrasena,
                "nombre": nombre.strip(),
            }
            st.success("Registro completado. Ya puedes iniciar sesión.")

    if st.button("Volver a iniciar sesión", key="volver_login"):
        st.session_state.vista_publica = "login"
        st.rerun()
