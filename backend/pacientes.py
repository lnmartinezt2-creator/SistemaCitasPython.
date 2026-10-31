from backend.database import conectar


def registrar_paciente(nombre, documento, edad, telefono, correo):
    """Guarda un paciente en la base de datos."""
    with conectar() as conexion:
        conexion.execute(
            """
            INSERT INTO pacientes
            (nombre, documento, edad, telefono, correo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, documento, edad, telefono, correo)
        )
        conexion.commit()