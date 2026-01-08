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
    """
    Ruta que maneja la actualización del estado de la tarea (CRUD Update).
    <int:tarea_id> es un parámetro dinámico que Flask espera en la URL.
    """
    # 1. Llamamos al método UPDATE del DBManager
    db_manager.actualizar_tarea_estado(tarea_id, "Completada")
    
    # 2. Redirigimos al usuario a la página principal para ver el cambio
    return redirect(url_for('index'))

@app.route('/eliminar/<int:tarea_id>')
def eliminar_tarea(tarea_id):
    """
    Ruta que maneja la eliminación de una tarea (CRUD Delete).
    <int:tarea_id> es un parámetro dinámico que Flask espera en la URL.
    """
    # 1. Llamamos al método DELETE del DBManager
    db_manager.eliminar_tarea(tarea_id)
    
    # 2. Redirigimos al usuario a la página principal para ver el cambio
    return redirect(url_for('index'))

@app.route('/proyecto/nuevo', methods=['GET', 'POST'])
def crear_proyecto_web():
    """Ruta para mostrar y procesar el formulario de nuevo proyecto."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        nuevo_p = Proyecto(nombre=nombre, descripcion=descripcion)
        db_manager.crear_proyecto(nuevo_p)
        return redirect(url_for('index'))
        
    return render_template('formulario_proyecto.html')

@app.route('/tarea/editar/<int:tarea_id>', methods=['GET', 'POST'])
def editar_tarea_web(tarea_id):
    tarea = db_manager.obtener_tarea_por_id(tarea_id)
    proyectos = db_manager.obtener_proyectos()

    if request.method == 'POST':
        
        tarea.actualizar_datos(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            fecha_limite=request.form.get('fecha_limite'),
            prioridad=request.form.get('prioridad'),
            proyecto_id=int(request.form.get('proyecto_id'))
        )
        
        db_manager.guardar_cambios_tarea(tarea)
        
        return redirect(url_for('index'))

    return render_template('formulario_edicion_tarea.html', tarea=tarea, proyectos=proyectos)

if __name__ == '__main__':
    # Las tablas ya se crean automáticamente en el __init__ de DBManager

    # Corremos Flask
    app.run(debug=True)

# app.py (después de las rutas existentes)