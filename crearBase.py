"""Modulo para inicializar la base de datos de alumnos.

Al ejecutarse como script crea (si no existe) la base de datos SQLite
requerida por la aplicacion principal.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

# Ruta al archivo de base de datos (en el mismo directorio que este script).
DB_PATH = Path(__file__).with_name("alumnos.db")


def crear_base() -> None:
    """Crea la tabla ``alumnos`` si todavia no existe."""
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                domicilio TEXT NOT NULL,
                dni TEXT NOT NULL UNIQUE,
                edad INTEGER NOT NULL
            )
            """
        )
        conexion.commit()


if __name__ == "__main__":
    crear_base()
    print(f"Base de datos inicializada en: {DB_PATH}")
