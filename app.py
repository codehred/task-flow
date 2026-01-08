from flask import Flask, render_template, request, redirect, url_for
from src.database import DBManager
from src.modelos import Tarea, Proyecto


app = Flask(__name__)
db_manager = DBManager()


@app.route('/')
def index():
    tareas_pendientes = db_manager.obtener_tareas(estado="Pendiente")
    proyectos = db_manager.obtener_proyectos()

    return render_template('index.html',
                           tareas=tareas_pendientes,
                           proyectos=proyectos)


@app.route('/crear', methods=['GET', 'POST'])
def crear_tarea_web():

    proyectos = db_manager.obtener_proyectos()

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        limite = request.form.get('fecha_limite')
        prioridad = request.form.get('prioridad')

        proyecto_id = int(request.form.get('proyecto_id'))

        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_limite=limite,
            prioridad=prioridad,
            proyecto_id=proyecto_id
        )

        db_manager.crear_tarea(nueva_tarea)

        return redirect(url_for('index'))

    return render_template('formulario_tarea.html', proyectos=proyectos)


@app.route('/completar/<int:tarea_id>')
def completar_tarea(tarea_id):
    db_manager.actualizar_tarea_estado(tarea_id, "Completada")

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Las tablas ya se crean automáticamente en el __init__ de DBManager

    # Corremos Flask
    app.run(debug=True)

# app.py (después de las rutas existentes)

@app.route('/completar/<int:tarea_id>')
def completar_tarea(tarea_id):
    """
    Ruta que maneja la actualización del estado de la tarea (CRUD Update).
    <int:tarea_id> es un parámetro dinámico que Flask espera en la URL.
    """
    # 1. Llamamos al método UPDATE del DBManager
    db_manager.actualizar_tarea_estado(tarea_id, "Completada")
    
    # 2. Redirigimos al usuario a la página principal para ver el cambio
    return redirect(url_for('index'))