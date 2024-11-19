from flask import Flask, render_template, request, redirect, url_for
from config import Config
from database import db
from models import Perfil, Publicacion, Grupo  # Asegúrate de importar Grupo correctamente
import os  # Para manejar rutas de archivos
from werkzeug.utils import secure_filename  # Para asegurar los nombres de archivos

# Configuración para subir imágenes
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión válida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inicializar la app
app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)  # Inicializa SQLAlchemy con la app

@app.route('/')
def inicio():
    """Página de inicio"""
    return render_template('index.html')

# Ruta para mostrar todos los perfiles con filtros y número de publicaciones
@app.route('/perfiles', methods=['GET'])
def mostrar_perfiles():
    filtro_nombre = request.args.get('nombre', '')
    filtro_apellido = request.args.get('apellido', '')
    ordenar_por = request.args.get('ordenar', '')

    # Consulta base
    query = Perfil.query

    # Filtrar por nombre
    if filtro_nombre:
        query = query.filter(Perfil.nombre.like(f"%{filtro_nombre}%"))

    # Filtrar por apellido
    if filtro_apellido:
        query = query.filter(Perfil.apellido.like(f"%{filtro_apellido}%"))

    # Ordenar por popularidad (número de publicaciones)
    if ordenar_por == 'popularidad':
        query = query.outerjoin(Publicacion, Perfil.id == Publicacion.usuario_id)\
                     .group_by(Perfil.id)\
                     .order_by(db.func.count(Publicacion.id).desc())

    perfiles = query.all()

    # Procesar datos para incluir número de publicaciones
    for perfil in perfiles:
        perfil.numero_publicaciones = Publicacion.query.filter_by(usuario_id=perfil.id).count()

    return render_template('perfiles.html', perfiles=perfiles)

# Ruta para editar un perfil
@app.route('/perfiles/<int:id>/editar', methods=['GET', 'POST'])
def editar_perfil(id):
    """Editar un perfil existente, incluyendo subir una nueva foto"""
    perfil = Perfil.query.get(id)
    if not perfil:
        return "Perfil no encontrado", 404

    if request.method == 'POST':
        perfil.nombre = request.form['nombre']
        perfil.apellido = request.form['apellido']
        perfil.fecha_nacimiento = request.form['fecha_nacimiento']
        perfil.genero = request.form['genero']
        perfil.correo_electronico = request.form['correo_electronico']

        # Manejar la subida de imagen
        if 'foto_perfil' in request.files:
            file = request.files['foto_perfil']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                perfil.foto_perfil = f'images/{filename}'  # Guarda la ruta relativa

        db.session.commit()
        return redirect(url_for('mostrar_perfiles'))

    return render_template('editar_perfil.html', perfil=perfil)

# Ruta para eliminar un perfil
@app.route('/perfiles/<int:id>/eliminar', methods=['POST'])
def eliminar_perfil(id):
    """Eliminar un perfil desde el botón"""
    perfil = Perfil.query.get(id)
    if not perfil:
        return "Perfil no encontrado", 404

    db.session.delete(perfil)
    db.session.commit()
    return redirect(url_for('mostrar_perfiles'))

# Ruta para mostrar publicaciones de un perfil específico
@app.route('/perfiles/<int:id>/publicaciones', methods=['GET'])
def ver_publicaciones(id):
    """Ver publicaciones de un perfil"""
    perfil = Perfil.query.get(id)
    if not perfil:
        return "Perfil no encontrado", 404

    publicaciones = Publicacion.query.filter_by(usuario_id=id).all()

    # Manejar el caso en que no haya publicaciones
    if not publicaciones:
        mensaje = "Este perfil no tiene publicaciones."
        return render_template('publicaciones.html', perfil=perfil, publicaciones=None, mensaje=mensaje)

    return render_template('publicaciones.html', perfil=perfil, publicaciones=publicaciones)

# Ruta para mostrar grupos con filtros
@app.route('/grupos', methods=['GET'])
def ver_grupos():
    """Ver la lista de grupos disponibles con filtros"""
    filtro_categoria = request.args.get('categoria', '')
    ordenar_por = request.args.get('ordenar', '')

    # Consulta base
    query = Grupo.query

    # Filtrar por categoría
    if filtro_categoria:
        query = query.filter(Grupo.categoria.like(f"%{filtro_categoria}%"))

    # Ordenar por popularidad (número de miembros)
    if ordenar_por == 'popularidad':
        query = query.order_by(Grupo.numero_miembros.desc())

    grupos = query.all()

    return render_template('grupos.html', grupos=grupos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True)
