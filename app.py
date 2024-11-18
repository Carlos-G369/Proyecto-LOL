from flask import Flask, render_template, request, redirect, session
from db import (
    crear_perfil, iniciar_sesion, crear_publicacion, crear_grupo, 
    actualizar_perfil, actualizar_publicacion, actualizar_grupo
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        genero = request.form['genero']
        correo_electronico = request.form['correo_electronico']
        contraseña = request.form['contraseña']
        mensaje = crear_perfil(nombre, apellido, fecha_nacimiento, genero, correo_electronico, contraseña)
        return render_template('register.html', mensaje=mensaje)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        contraseña = request.form['contraseña']
        usuario_id = iniciar_sesion(correo_electronico, contraseña)
        if usuario_id:
            session['usuario_id'] = usuario_id
            return redirect('/profile')
        else:
            mensaje = "Correo electrónico o contraseña incorrectos."
            return render_template('login.html', mensaje=mensaje)
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'usuario_id' in session:
        return render_template('profile.html')
    else:
        return redirect('/login')

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'usuario_id' in session:
        if request.method == 'POST':
            usuario_id = session['usuario_id']
            titulo_publicacion = request.form['titulo_publicacion']
            contenido = request.form['contenido']
            mensaje = crear_publicacion(usuario_id, titulo_publicacion, contenido)
            return render_template('publication.html', mensaje=mensaje)
        return render_template('publication.html')
    else:
        return redirect('/login')

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if 'usuario_id' in session:
        if request.method == 'POST':
            usuario_id = session['usuario_id']
            nombre_grupo = request.form['nombre_grupo']
            descripcion = request.form['descripcion']
            privacidad = request.form['privacidad']
            mensaje = crear_grupo(usuario_id, nombre_grupo, descripcion, privacidad)
            return render_template('group.html', mensaje=mensaje)
        return render_template('group.html')
    else:
        return redirect('/login')

# Ruta para actualizar perfil
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'usuario_id' in session:
        if request.method == 'POST':
            usuario_id = session['usuario_id']
            nuevo_nombre = request.form.get('nuevo_nombre')
            nuevo_apellido = request.form.get('nuevo_apellido')
            nuevo_fecha_nacimiento = request.form.get('nuevo_fecha_nacimiento')
            nuevo_genero = request.form.get('nuevo_genero')
            nuevo_correo_electronico = request.form.get('nuevo_correo_electronico')
            nuevo_contraseña = request.form.get('nuevo_contraseña')
            mensaje = actualizar_perfil(
                usuario_id, nuevo_nombre, nuevo_apellido, nuevo_fecha_nacimiento, nuevo_genero, nuevo_correo_electronico, nuevo_contraseña
            )
            return render_template('update_profile.html', mensaje=mensaje)
        return render_template('update_profile.html')
    else:
        return redirect('/login')

# Ruta para actualizar publicación
@app.route('/update_post', methods=['GET', 'POST'])
def update_post():
    if 'usuario_id' in session:
        if request.method == 'POST':
            post_id = request.form['post_id']
            nuevo_titulo = request.form.get('nuevo_titulo')
            nuevo_contenido = request.form.get('nuevo_contenido')
            mensaje = actualizar_publicacion(post_id, nuevo_titulo, nuevo_contenido)
            return render_template('update_post.html', mensaje=mensaje)
        return render_template('update_post.html')
    else:
        return redirect('/login')

# Ruta para actualizar grupo
@app.route('/update_group', methods=['GET', 'POST'])
def update_group():
    if 'usuario_id' in session:
        if request.method == 'POST':
            grupo_id = request.form['grupo_id']
            nuevo_nombre_grupo = request.form.get('nuevo_nombre_grupo')
            nueva_descripcion = request.form.get('nueva_descripcion')
            nueva_privacidad = request.form.get('nueva_privacidad')
            mensaje = actualizar_grupo(grupo_id, nuevo_nombre_grupo, nueva_descripcion, nueva_privacidad)
            return render_template('update_group.html', mensaje=mensaje)
        return render_template('update_group.html')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
