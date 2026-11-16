import sqlite3

from alumno import Alumno
from curso import Curso
from matricula import Matricula


# ==========================================================
# 1. CONEXION Y CONFIGURACION DE LA BASE DE DATOS
# ==========================================================

conexion = sqlite3.connect("inacap.db")
cursor = conexion.cursor()

# SQLite no activa las claves foraneas automaticamente.
cursor.execute("PRAGMA foreign_keys = ON")

print("==========================================")
print(" CONEXION CON BASE DE DATOS")
print("==========================================")
print("Conexion realizada correctamente.")


try:
    # ======================================================
    # 2. CREACION DE TABLAS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            edad INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS curso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            horas INTEGER
        )
    """)

    # Compatibilidad con la version anterior de la tabla,
    # que utilizaba el nombre de columna "hora".
    columnas_curso = [
        columna[1] for columna in cursor.execute(
            "PRAGMA table_info(curso)"
        ).fetchall()
    ]
    if "hora" in columnas_curso and "horas" not in columnas_curso:
        cursor.execute("ALTER TABLE curso RENAME COLUMN hora TO horas")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matricula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (alumno_id) REFERENCES alumno(id),
            FOREIGN KEY (curso_id) REFERENCES curso(id)
        )
    """)

    conexion.commit()

    print("Tablas alumno, curso y matricula creadas correctamente.")

    # ======================================================
    # 3. CRUD ALUMNO
    # ======================================================

    print("\n========== CRUD ALUMNO ==========")

    # CREATE: insertar alumnos
    alumno1 = Alumno(None, "Juan Perez", "juan@gmail.com", 21)
    alumno2 = Alumno(None, "Maria Gonzalez", "maria@gmail.com", 22)

    cursor.execute(
        """
        INSERT INTO alumno (nombre, email, edad)
        VALUES (?, ?, ?)
        """,
        (alumno1.nombre, alumno1.email, alumno1.edad)
    )
    alumno1.id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO alumno (nombre, email, edad)
        VALUES (?, ?, ?)
        """,
        (alumno2.nombre, alumno2.email, alumno2.edad)
    )
    alumno2.id = cursor.lastrowid
    conexion.commit()

    print("Alumnos insertados correctamente.")

    # READ: mostrar alumnos
    cursor.execute("SELECT id, nombre, email, edad FROM alumno")
    alumnos = cursor.fetchall()

    print("\nLISTADO DE ALUMNOS")
    for fila in alumnos:
        print(
            f"ID: {fila[0]} | Nombre: {fila[1]} | "
            f"Email: {fila[2]} | Edad: {fila[3]}"
        )

    # UPDATE: actualizar alumnos
    cursor.execute(
        "UPDATE alumno SET email = ? WHERE id = ?",
        ("juan.perez@gmail.com", alumno1.id)
    )
    cursor.execute(
        "UPDATE alumno SET edad = ? WHERE id = ?",
        (23, alumno2.id)
    )
    conexion.commit()
    print("\nAlumnos actualizados correctamente.")

    # READ: comprobar actualizaciones
    cursor.execute("SELECT id, nombre, email, edad FROM alumno")
    print("\nALUMNOS DESPUES DEL UPDATE")
    for fila in cursor.fetchall():
        print(
            f"ID: {fila[0]} | Nombre: {fila[1]} | "
            f"Email: {fila[2]} | Edad: {fila[3]}"
        )

    # ======================================================
    # 4. CRUD CURSO
    # ======================================================

    print("\n========== CRUD CURSO ==========")

    # CREATE: insertar cursos
    curso1 = Curso(None, "Python", 60)
    curso2 = Curso(None, "Base de Datos", 50)

    cursor.execute(
        "INSERT INTO curso (nombre, horas) VALUES (?, ?)",
        (curso1.nombre, curso1.horas)
    )
    curso1.id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO curso (nombre, horas) VALUES (?, ?)",
        (curso2.nombre, curso2.horas)
    )
    curso2.id = cursor.lastrowid
    conexion.commit()

    print("Cursos insertados correctamente.")

    # READ: mostrar cursos
    cursor.execute("SELECT id, nombre, horas FROM curso")
    print("\nLISTADO DE CURSOS")
    for fila in cursor.fetchall():
        print(f"ID: {fila[0]} | Curso: {fila[1]} | Horas: {fila[2]}")

    # UPDATE: actualizar cursos
    cursor.execute(
        "UPDATE curso SET horas = ? WHERE id = ?",
        (70, curso1.id)
    )
    cursor.execute(
        "UPDATE curso SET nombre = ? WHERE id = ?",
        ("Bases de Datos SQL", curso2.id)
    )
    conexion.commit()
    print("\nCursos actualizados correctamente.")

    # READ: comprobar actualizaciones
    cursor.execute("SELECT id, nombre, horas FROM curso")
    print("\nCURSOS DESPUES DEL UPDATE")
    for fila in cursor.fetchall():
        print(f"ID: {fila[0]} | Curso: {fila[1]} | Horas: {fila[2]}")

    # ======================================================
    # 5. CRUD MATRICULA
    # ======================================================

    print("\n========== CRUD MATRICULA ==========")

    # CREATE: insertar matriculas usando los ID reales
    matricula1 = Matricula(None, alumno1.id, curso1.id, "2026-09-22")
    matricula2 = Matricula(None, alumno2.id, curso2.id, "2026-09-22")

    cursor.execute(
        """
        INSERT INTO matricula (alumno_id, curso_id, fecha)
        VALUES (?, ?, ?)
        """,
        (matricula1.alumno_id, matricula1.curso_id, matricula1.fecha)
    )
    matricula1.id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO matricula (alumno_id, curso_id, fecha)
        VALUES (?, ?, ?)
        """,
        (matricula2.alumno_id, matricula2.curso_id, matricula2.fecha)
    )
    matricula2.id = cursor.lastrowid
    conexion.commit()

    print("Matriculas insertadas correctamente.")

    # READ: mostrar matriculas
    cursor.execute("""
        SELECT id, alumno_id, curso_id, fecha
        FROM matricula
    """)
    print("\nLISTADO DE MATRICULAS")
    for fila in cursor.fetchall():
        print(
            f"ID: {fila[0]} | Alumno ID: {fila[1]} | "
            f"Curso ID: {fila[2]} | Fecha: {fila[3]}"
        )

    # UPDATE: actualizar fechas
    cursor.execute(
        "UPDATE matricula SET fecha = ? WHERE id = ?",
        ("2026-09-23", matricula1.id)
    )
    cursor.execute(
        "UPDATE matricula SET fecha = ? WHERE id = ?",
        ("2026-09-24", matricula2.id)
    )
    conexion.commit()
    print("\nMatriculas actualizadas correctamente.")

    # READ: comprobar actualizaciones
    cursor.execute("""
        SELECT id, alumno_id, curso_id, fecha
        FROM matricula
    """)
    print("\nMATRICULAS DESPUES DEL UPDATE")
    for fila in cursor.fetchall():
        print(
            f"ID: {fila[0]} | Alumno ID: {fila[1]} | "
            f"Curso ID: {fila[2]} | Fecha: {fila[3]}"
        )

    # ======================================================
    # 6. DELETE
    # ======================================================
    # Primero se eliminan las matriculas porque dependen
    # de alumnos y cursos mediante claves foraneas.

    print("\n========== DELETE ==========")

    cursor.execute("DELETE FROM matricula WHERE id = ?", (matricula1.id,))
    cursor.execute("DELETE FROM matricula WHERE id = ?", (matricula2.id,))
    conexion.commit()
    print("Matriculas eliminadas correctamente.")

    cursor.execute("DELETE FROM alumno WHERE id = ?", (alumno1.id,))
    cursor.execute("DELETE FROM alumno WHERE id = ?", (alumno2.id,))
    conexion.commit()
    print("Alumnos eliminados correctamente.")

    cursor.execute("DELETE FROM curso WHERE id = ?", (curso1.id,))
    cursor.execute("DELETE FROM curso WHERE id = ?", (curso2.id,))
    conexion.commit()
    print("Cursos eliminados correctamente.")

    print("\n==========================================")
    print(" PROCESO TERMINADO")
    print("==========================================")

except Exception:
    conexion.rollback()
    raise

finally:
    cursor.close()
    conexion.close()
    print("Conexion cerrada correctamente.")
