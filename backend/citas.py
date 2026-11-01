
from backend.database import conectar


def registrar_cita(paciente_id, fecha, hora, motivo):
    """Guarda una nueva cita médica en SQLite."""

    with conectar() as conexion:
        conexion.execute(
            """
            INSERT INTO citas
            (paciente_id, fecha, hora, motivo, estado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                paciente_id,
                fecha,
                hora,
                motivo,
                "Programada"
            )
        )
        conexion.commit()


def listar_citas():
    """Consulta las citas con el nombre del paciente."""

    with conectar() as conexion:
        cursor = conexion.execute(
            """
            SELECT
                citas.id,
                pacientes.nombre,
                citas.fecha,
                citas.hora,
                citas.motivo,
                citas.estado
            FROM citas
            INNER JOIN pacientes
                ON citas.paciente_id = pacientes.id
            ORDER BY citas.fecha, citas.hora
            """
        )

        return cursor.fetchall()
