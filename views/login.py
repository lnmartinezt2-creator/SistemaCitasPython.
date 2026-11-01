
            
import streamlit as st


def mostrar_login() -> None:
    # Contenedor principal del inicio de sesión
    with st.container(border=True):
        st.title("Sistema de Gestión de Citas")
        st.subheader("Iniciar sesión")

        # Formulario de inicio de sesión
        with st.form("formulario_login"):
            usuario = st.text_input("Usuario")
            contrasena = st.text_input(
                "Contraseña",
                type="password"
            )
            ingresar = st.form_submit_button("Ingresar")

        # Validación de usuario y contraseña
        if ingresar:
            usuario_limpio = usuario.strip().lower()

            datos_usuario = st.session_state.usuarios.get(
                usuario_limpio
            )

            if (
                datos_usuario
                and datos_usuario["contrasena"] == contrasena
            ):
                st.session_state.sesion_iniciada = True
                st.session_state.usuario_actual = datos_usuario["nombre"]
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

    
    # Enlaces debajo del formulario
    col_registro, col_olvido = st.columns([1, 1], gap="small")

    with col_registro:
        if st.button(
            "¿No tienes cuenta? Regístrate",
            key="ir_registro",
            type="tertiary"
        ):
            st.session_state.vista_publica = "registro"
            st.rerun()

    with col_olvido:
        with st.container(
            horizontal=True,
            horizontal_alignment="right"
        ):
            if st.button(
                "¿Se te olvidó tu contraseña?",
                key="recuperar",
                type="tertiary"
            ):
                st.info(
                    "La recuperación de contraseña estará disponible próximamente."
                )
