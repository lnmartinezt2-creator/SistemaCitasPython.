
import sqlite3
from datetime import date, datetime

import streamlit as st

from backend.database import crear_tablas
from backend.pacientes import (
    registrar_paciente,
    listar_pacientes,
    actualizar_paciente,
    eliminar_paciente,
)
from backend.citas import (
    registrar_cita,
    listar_citas,
    actualizar_cita,
    cancelar_cita,
)


# Crear las tablas de la base de datos
crear_tablas()


def mostrar_dashboard() -> None:
    """Muestra el panel principal del sistema."""

    st.title("Sistema de Gestión de Citas")

    st.success(
        f"Bienvenido, {st.session_state.get('usuario_actual', 'usuario')}."
    )

    opcion = st.sidebar.radio(
        "Menú principal",
        ["Inicio", "Pacientes", "Gestión de citas"]
    )

    if opcion == "Inicio":
        st.header("Panel principal")
        st.write("Bienvenido al Sistema de Gestión de Citas.")

    elif opcion == "Pacientes":
        mostrar_pacientes()

    elif opcion == "Gestión de citas":
        mostrar_citas()

    # CERRAR SESIÓN
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.sesion_iniciada = False
        st.session_state.pop("usuario_actual", None)
        st.rerun()


def mostrar_pacientes() -> None:
    """Permite registrar, consultar, editar y eliminar pacientes."""

    st.header("Gestión de pacientes")

    # ==========================================
    # 1. REGISTRAR PACIENTES
    # ==========================================

    st.subheader("Registro de pacientes")

    with st.form("formulario_pacientes"):

        nombre = st.text_input("Nombre completo")
        documento = st.text_input("Número de documento")

        edad = st.number_input(
            "Edad",
            min_value=0,
            max_value=120
        )

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

                st.success("Paciente guardado correctamente.")

            except sqlite3.IntegrityError:
                st.error(
                    "Ya existe un paciente con ese documento."
                )

        else:
            st.error(
                "Debe ingresar el nombre y el documento."
            )

    # ==========================================
    # 2. CONSULTAR PACIENTES
    # ==========================================

    st.subheader("Lista de pacientes registrados")

    pacientes = listar_pacientes()

    if pacientes:

        columnas = [
            "ID",
            "Nombre",
            "Documento",
            "Edad",
            "Teléfono",
            "Correo"
        ]

        datos = [
            dict(zip(columnas, paciente))
            for paciente in pacientes
        ]

        st.dataframe(
            datos,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No hay pacientes registrados todavía.")

    # ==========================================
    # 3. EDITAR PACIENTES
    # ==========================================

    if pacientes:

        st.subheader("Editar paciente")

        opciones_editar = {
            f"{p[1]} - Documento: {p[2]}": p
            for p in pacientes
        }

        seleccionado = st.selectbox(
            "Selecciona el paciente que deseas editar",
            options=list(opciones_editar.keys()),
            key="seleccionar_editar"
        )

        paciente = opciones_editar[seleccionado]

        with st.form("formulario_editar_paciente"):

            nuevo_nombre = st.text_input(
                "Nombre completo",
                value=paciente[1]
            )

            nuevo_documento = st.text_input(
                "Número de documento",
                value=paciente[2]
            )

            nueva_edad = st.number_input(
                "Edad",
                min_value=0,
                max_value=120,
                value=int(paciente[3] or 0)
            )

            nuevo_telefono = st.text_input(
                "Teléfono",
                value=paciente[4] or ""
            )

            nuevo_correo = st.text_input(
                "Correo electrónico",
                value=paciente[5] or ""
            )

            guardar_cambios = st.form_submit_button(
                "Guardar cambios"
            )

        if guardar_cambios:

            if nuevo_nombre.strip() and nuevo_documento.strip():

                try:
                    actualizado = actualizar_paciente(
                        paciente[0],
                        nuevo_nombre.strip(),
                        nuevo_documento.strip(),
                        nueva_edad,
                        nuevo_telefono.strip(),
                        nuevo_correo.strip()
                    )

                    if actualizado:
                        st.success(
                            "Paciente actualizado correctamente."
                        )
                        st.rerun()

                    else:
                        st.error("No se encontró el paciente.")

                except sqlite3.IntegrityError:
                    st.error(
                        "Ya existe otro paciente con ese documento."
                    )

            else:
                st.error(
                    "El nombre y el documento son obligatorios."
                )

    # ==========================================
    # 4. ELIMINAR PACIENTES
    # ==========================================

    if pacientes:

        st.subheader("Eliminar paciente")

        opciones_eliminar = {
            f"{p[1]} - Documento: {p[2]}": p[0]
            for p in pacientes
        }

        paciente_seleccionado = st.selectbox(
            "Selecciona el paciente que deseas eliminar",
            options=list(opciones_eliminar.keys()),
            key="seleccionar_eliminar"
        )

        confirmar = st.checkbox(
            "Confirmo que deseo eliminar este paciente"
        )

        if confirmar:

            if st.button(
                "Eliminar paciente",
                type="primary"
            ):

                paciente_id = opciones_eliminar[
                    paciente_seleccionado
                ]

                eliminado = eliminar_paciente(paciente_id)

                if eliminado:
                    st.success(
                        "Paciente eliminado correctamente."
                    )
                    st.rerun()

                else:
                    st.error(
                        "No se pudo eliminar el paciente."
                    )


def mostrar_citas() -> None:
    """Permite registrar y consultar citas médicas."""

    st.header("Gestión de citas")
    st.subheader("Programar nueva cita")

    # CONSULTAR PACIENTES REGISTRADOS
    pacientes = listar_pacientes()

    if not pacientes:
        st.warning(
            "Primero debes registrar un paciente "
            "en la sección Pacientes."
        )
        return

    opciones = {
        f"{p[1]} - Documento: {p[2]}": p[0]
        for p in pacientes
    }

    # ==========================================
    # 5. PROGRAMAR CITAS
    # ==========================================

    with st.form("formulario_citas"):

        paciente_seleccionado = st.selectbox(
            "Selecciona el paciente",
            options=list(opciones.keys())
        )

        fecha_cita = st.date_input(
            "Fecha de la cita",
            value=date.today(),
            min_value=date.today()
        )

        hora_cita = st.time_input(
            "Hora de la cita"
        )

        motivo = st.text_area(
            "Motivo de la consulta"
        )

        guardar_cita = st.form_submit_button(
            "Programar cita"
        )

    if guardar_cita:

        if not motivo.strip():
            st.error(
                "Debes escribir el motivo de la consulta."
            )

        elif datetime.combine(
            fecha_cita, hora_cita
        ) <= datetime.now():

            st.error(
                "La fecha y hora de la cita deben ser futuras."
            )

        else:

            paciente_id = opciones[paciente_seleccionado]

            registrar_cita(
                paciente_id,
                fecha_cita.isoformat(),
                hora_cita.strftime("%H:%M"),
                motivo.strip()
            )

            st.success(
                "Cita programada correctamente."
            )
            st.rerun()

    # ==========================================
    # 6. CONSULTAR CITAS
    # ==========================================

    st.subheader("Citas programadas")

    citas = listar_citas()

    if citas:

        columnas = [
            "ID",
            "Paciente",
            "Fecha",
            "Hora",
            "Motivo",
            "Estado"
        ]

        datos = [
            dict(zip(columnas, cita))
            for cita in citas
        ]

        st.dataframe(
            datos,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "Todavía no hay citas programadas."
        )
        
        
    # ==========================================
    # MODIFICAR Y CANCELAR CITAS
    # ==========================================

    if citas:

        citas_programadas = [
            cita for cita in citas
            if cita[5] == "Programada"
        ]

        if citas_programadas:

            opciones_citas = {
                f"Cita {c[0]} - {c[1]} - {c[2]}": c
                for c in citas_programadas
            }

            # MODIFICAR CITA
            st.subheader("Modificar cita")

            seleccion = st.selectbox(
                "Selecciona la cita que deseas modificar",
                options=list(opciones_citas.keys()),
                key="editar_cita"
            )

            cita = opciones_citas[seleccion]

            with st.form("formulario_editar_cita"):

                nueva_fecha = st.date_input(
                    "Nueva fecha",
                    value=max(
                        date.fromisoformat(cita[2]),
                        date.today()
                    ),
                    min_value=date.today()
                )

                nueva_hora = st.time_input(
                    "Nueva hora",
                    value=datetime.strptime(
                        cita[3], "%H:%M"
                    ).time()
                )

                nuevo_motivo = st.text_area(
                    "Motivo de la consulta",
                    value=cita[4]
                )

                guardar_cambios = st.form_submit_button(
                    "Guardar cambios de la cita"
                )

            if guardar_cambios:

                if not nuevo_motivo.strip():
                    st.error("El motivo es obligatorio.")

                elif datetime.combine(
                    nueva_fecha, nueva_hora
                ) <= datetime.now():
                    st.error(
                        "La fecha y hora deben ser futuras."
                    )

                else:
                    actualizado = actualizar_cita(
                        cita[0],
                        nueva_fecha.isoformat(),
                        nueva_hora.strftime("%H:%M"),
                        nuevo_motivo.strip()
                    )

                    if actualizado:
                        st.success("Cita actualizada correctamente.")
                        st.rerun()
                    else:
                        st.error("No se pudo actualizar la cita.")

            # CANCELAR CITA
            st.subheader("Cancelar cita")

            seleccion_cancelar = st.selectbox(
                "Selecciona la cita que deseas cancelar",
                options=list(opciones_citas.keys()),
                key="cancelar_cita"
            )

            confirmar = st.checkbox(
                "Confirmo que deseo cancelar esta cita"
            )

            if confirmar and st.button("Cancelar cita"):

                cita_seleccionada = opciones_citas[
                    seleccion_cancelar
                ]

                cancelada = cancelar_cita(
                    cita_seleccionada[0]
                )

                if cancelada:
                    st.success("Cita cancelada correctamente.")
                    st.rerun()
                else:
                    st.error("No se pudo cancelar la cita.")

        else:
            st.info(
                "No hay citas programadas para modificar o cancelar."
            )

