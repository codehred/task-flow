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
    todos = db_manager.obtener_proyectos()

    proyectos_validos = [p for p in todos if p._estado == 'Activo' or p._id == 0]

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        limite = request.form.get('fecha_limite')
        prioridad = request.form.get('prioridad')
        proyecto_id = int(request.form.get('proyecto_id'))

        nueva_tarea = Tarea(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            fecha_limite=request.form.get('fecha_limite'),
            prioridad=request.form.get('prioridad'),
            proyecto_id=int(request.form.get('proyecto_id'))
        )
        db_manager.crear_tarea(nueva_tarea)
        return redirect(url_for('index'))

    return render_template('formulario_tarea.html', proyectos=proyectos_validos)



@app.route('/completar/<int:tarea_id>')
def completar_tarea(tarea_id):
    
   
    db_manager.actualizar_tarea_estado(tarea_id, "Completada")
    
   
    return redirect(url_for('index'))

@app.route('/eliminar/<int:tarea_id>')
def eliminar_tarea(tarea_id):
   
    db_manager.eliminar_tarea(tarea_id)
    

    return redirect(url_for('index'))

@app.route('/proyecto/nuevo', methods=['GET', 'POST'])
def crear_proyecto_web():
    
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

@app.route('/proyecto/editar/<int:proyecto_id>', methods=['GET', 'POST'])
def editar_proyecto_web(proyecto_id):
    proyecto = db_manager.obtener_proyecto_por_id(proyecto_id)

    if request.method == 'POST':
        
        proyecto.actualizar_datos(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            estado=request.form.get('estado')
        )
        
        db_manager.guardar_cambios_proyecto(proyecto)
        
        return redirect(url_for('index'))

    return render_template('formulario_edicion_proyecto.html', proyecto=proyecto)

@app.route('/proyecto/eliminar/<int:proyecto_id>')
def eliminar_proyecto_web(proyecto_id):
    db_manager.eliminar_proyecto(proyecto_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Las tablas ya se crean automáticamente en el __init__ de DBManager

    # Corremos Flask
    app.run(debug=True)

# app.py (después de las rutas existentes)