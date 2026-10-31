
import sqlite3
from pathlib import Path

RUTA_DB = Path(__file__).resolve().parent / "citas.db"


def conectar():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect(RUTA_DB)


def crear_tablas():
    """Crea las tablas necesarias si todavía no existen."""
    with conectar() as conexion:
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
        conexion.commit()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos creada correctamente.")
