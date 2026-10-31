import streamlit as st


def mostrar_login() -> None:
    with st.container(border=True):
        st.title("Sistema de Gestión de Citas")
        st.subheader("Iniciar sesión")

        with st.form("formulario_login"):
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            ingresar = st.form_submit_button("Ingresar")

        if ingresar:
            usuario_limpio = usuario.strip().lower()
            datos_usuario = st.session_state.usuarios.get(usuario_limpio)

            if datos_usuario and datos_usuario["contrasena"] == contrasena:
                st.session_state.sesion_iniciada = True
                st.session_state.usuario_actual = datos_usuario["nombre"]
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

    col_olvido, col_registro = st.columns(2)

    with col_olvido:
        if st.button(
            "¿Se te olvidó tu contraseña?",
            key="recuperar",
            type="secondary",
        ):
            st.info("Recuperación disponible próximamente.")

    with col_registro:
        if st.button(
            "¿No tienes cuenta? Regístrate",
            key="ir_registro",
            type="secondary",
        ):
            st.session_state.vista_publica = "registro"
            st.rerun()