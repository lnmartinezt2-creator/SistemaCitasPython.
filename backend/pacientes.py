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
        
def listar_pacientes():
    """Obtiene los pacientes registrados en SQLite."""
    with conectar() as conexion:
        cursor = conexion.execute("""
            SELECT id, nombre, documento, edad, telefono, correo
            FROM pacientes
            ORDER BY id DESC
        """)
        return cursor.fetchall()
    
    
def eliminar_paciente(paciente_id):
    """Elimina un paciente de la base de datos."""
    with conectar() as conexion:
        cursor = conexion.execute(
            "DELETE FROM pacientes WHERE id = ?",
            (paciente_id,)
        )
        conexion.commit()
        return cursor.rowcount > 0
    
def actualizar_paciente(
    paciente_id, nombre, documento, edad, telefono, correo
):
    """Actualiza los datos de un paciente registrado."""

    with conectar() as conexion:
        cursor = conexion.execute(
            """
            UPDATE pacientes
            SET nombre = ?,
                documento = ?,
                edad = ?,
                telefono = ?,
                correo = ?
            WHERE id = ?
            """,
            (
                nombre,
                documento,
                edad,
                telefono,
                correo,
                paciente_id
            )
        )

        conexion.commit()
        return cursor.rowcount > 0


