import sqlite3
from .modelos import Tarea, Proyecto
import os

DATABASE_NAME = 'tareas.db'


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla proyectos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            estado TEXT
        )
    """)

    # Tabla tareas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEXT,
            fecha_limite TEXT,
            prioridad TEXT,
            estado TEXT,
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    try:
        cursor.execute(
            "INSERT INTO proyectos (id, nombre, descripcion, estado) VALUES (0, 'Tareas Generales', 'Tareas sin clasificar', 'Activo')")
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()


class DBManager:

    

    def __init__(self):
        crear_tablas()

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tareas(titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (tarea._titulo, tarea._descripcion, tarea._fecha_creacion, tarea._fecha_limite, tarea._prioridad, tarea._estado, tarea._proyecto_id))

        tarea.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea

    def obtener_proyectos(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos")
        filas = cursor.fetchall()
        conn.close()

        proyectos = [
            Proyecto(nombre=fila['nombre'], descripcion=fila['descripcion'],
                     id=fila['id'], estado=fila['estado'])
            for fila in filas
        ]
        return proyectos
    
    def crear_proyecto(self, proyecto: Proyecto) -> Proyecto:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proyectos(nombre, descripcion, fecha_inicio, estado)
            VALUES(?, ?, ?, ?)
        """, (proyecto._nombre, proyecto._descripcion,
              proyecto._fecha_inicio, proyecto._estado))

        proyecto.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return proyecto
    
    def eliminar_tarea(self, tarea_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))

        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()
        return deleted

    def obtener_tareas(self, estado=None):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM tareas"
        params = []

        if estado:
            sql += " WHERE estado = ?"
            params.append(estado)

        sql += " ORDER BY fecha_limite ASC"

        cursor.execute(sql, params)
        filas = cursor.fetchall()
        conn.close()

        tareas = []
        for fila in filas:
            t = Tarea(
                titulo=fila['titulo'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                proyecto_id=fila['proyecto_id'],
                estado=fila['estado'],
                descripcion=fila['descripcion'],
                fecha_creacion=fila['fecha_creacion'],
                id=fila['id']
            )
            tareas.append(t)
        return tareas

    def actualizar_tarea_estado(self, tarea_id: int, nuevo_estado: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tareas
            SET estado=?
            WHERE id=?
        """, (nuevo_estado, tarea_id))

        updated = cursor.rowcount > 0

        conn.commit()
        conn.close()
        return updated
    

     # --- Tareas (CRUD - UPDATE) ---
    def actualizar_tarea_estado(self, tarea_id: int, nuevo_estado: str) -> bool:
        """
        Actualiza el estado de una tarea específica en la DB. 
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL para actualizar UN solo campo de UN solo registro (UPDATE)
        cursor.execute("""
            UPDATE tareas 
            SET estado=?
            WHERE id=?
        """, (nuevo_estado, tarea_id))
        
        # Validamos si se actualizó algún registro
        updated = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return updated
    def actualizar_tarea_editar(self, tarea_id: int, nuevo_titulo: str, nueva_descripcion: str,
                                 nueva_fecha_limite: str, nueva_prioridad: str) -> bool:
        """
        Actualiza los detalles de una tarea específica en la DB.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL para actualizar varios campos de UN solo registro (UPDATE)
        cursor.execute("""
            UPDATE tareas 
            SET titulo=?, descripcion=?, fecha_limite=?, prioridad=?
            WHERE id=?
        """, (nuevo_titulo, nueva_descripcion, nueva_fecha_limite, nueva_prioridad, tarea_id))
        
        # Validamos si se actualizó algún registro
        updated = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return updated
    def obtener_tarea_por_id(self, tarea_id: int) -> Tarea:
        """
        Obtiene una tarea específica por su ID.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tareas WHERE id=?", (tarea_id,))
        fila = cursor.fetchone()
        conn.close()
        
        if fila:
            tarea = Tarea(
                titulo=fila['titulo'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                proyecto_id=fila['proyecto_id'],
                estado=fila['estado'],
                descripcion=fila['descripcion'],
                fecha_creacion=fila['fecha_creacion'],
                id=fila['id']
            )
            return tarea
        return None
    def guardar_cambios_tarea(self, tarea: Tarea):
        """Recibe un objeto Tarea y guarda sus cambios en la DB."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tareas 
            SET titulo=?, descripcion=?, fecha_limite=?, prioridad=?, proyecto_id=?
            WHERE id=?
        """, (tarea._titulo, tarea._descripcion, tarea._fecha_limite, 
            tarea._prioridad, tarea._proyecto_id, tarea._id))
        conn.commit()
        conn.close()  
    def obtener_proyecto_por_id(self, proyecto_id: int) -> Proyecto:
       
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM proyectos WHERE id=?", (proyecto_id,))
        fila = cursor.fetchone()
        conn.close()
        
        if fila:
            proyecto = Proyecto(
                nombre=fila['nombre'],
                descripcion=fila['descripcion'],
                id=fila['id'],
                estado=fila['estado']
            )
            return proyecto
        return None
    def guardar_cambios_proyecto(self, proyecto: Proyecto):
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proyectos 
            SET nombre=?, descripcion=?, estado=?
            WHERE id=?
        """, (proyecto._nombre, proyecto._descripcion, 
            proyecto._estado, proyecto._id))
        conn.commit()
        conn.close()
    def eliminar_proyecto(self, proyecto_id: int) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM proyectos WHERE id=?", (proyecto_id,))

        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()
        return deleted


if __name__ == '__main__':
    # Bloque de prueba para la clase
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Base de datos {DATABASE_NAME} eliminada.")

    crear_tablas()
    print(
        f"Base de datos {DATABASE_NAME} y tablas inicializadas correctamente.")

    # Prueba del CRUD (CREATE)
    manager = DBManager()
    tarea_prueba = Tarea(
        titulo="Completar Ejercicio de CRUD",
        fecha_limite="2025-10-30",
        prioridad="Alta",
        proyecto_id=0,
        descripcion="Implementar el módulo database.py"
    )

    tarea_creada = manager.crear_tarea(tarea_prueba)
    print(f"Tarea creada y ID asignado: {tarea_creada.id}")

    # src/database.py (dentro de la clase DBManager)

   