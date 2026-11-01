
import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent / "citas.db"


def conectar():
    """Establece la conexión con SQLite."""
    return sqlite3.connect(RUTA_DB)


def crear_tablas():
    """Crea las tablas de pacientes y citas."""

    with conectar() as conexion:

        # TABLA DE PACIENTES
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                documento TEXT NOT NULL UNIQUE,
                edad INTEGER,
                telefono TEXT,
                correo TEXT
            )
        """)

        # TABLA DE CITAS
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                motivo TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Programada',
                FOREIGN KEY (paciente_id)
                    REFERENCES pacientes(id)
            )
        """)

        conexion.commit()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos creada correctamente.")
