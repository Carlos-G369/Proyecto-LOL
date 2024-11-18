import mysql.connector
from mysql.connector import Error
import bcrypt

def conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="league_of_legends"
    )

# Función para crear perfil
def crear_perfil(nombre, apellido, fecha_nacimiento, genero, correo_electronico, contraseña):
    connex = conexion()
    cursor = connex.cursor()
    try:
        salt = bcrypt.gensalt()
        contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
        sql = "INSERT INTO perfil(nombre, apellido, fecha_nacimiento, genero, correo_electronico, contraseña) VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, apellido, fecha_nacimiento, genero, correo_electronico, contraseña_hash))
        connex.commit()
        return "Usuario creado exitosamente."
    except Error as e:
        return f"Error al crear usuario: {e}"
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()

# Función para iniciar sesión
def iniciar_sesion(correo_electronico, contraseña):
    connex = conexion()
    cursor = connex.cursor()
    try:
        sql = "SELECT id, contraseña FROM perfil WHERE correo_electronico = %s"
        cursor.execute(sql, (correo_electronico,))
        resultado = cursor.fetchone()
        if resultado:
            usuario_id, contraseña_hash = resultado
            if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hash.encode('utf-8')):
                return usuario_id
            else:
                return None
        else:
            return None
    except Error as e:
        return None
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()

# Función para crear publicación
def crear_publicacion(usuario_id, titulo_publicacion, contenido):
    connex = conexion()
    cursor = connex.cursor()
    try:
        sql = "INSERT INTO publicacion(usuario_id, titulo_publicacion, contenido) VALUES(%s, %s, %s)"
        cursor.execute(sql, (usuario_id, titulo_publicacion, contenido))
        connex.commit()
        return "Publicacion creada exitosamente."
    except Error as e:
        return f"Error al crear publicacion: {e}"
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()

# Función para crear grupo
def crear_grupo(usuario_id, nombre_grupo, descripcion, privacidad):
    connex = conexion()
    cursor = connex.cursor()
    try:
        sql = "INSERT INTO grupo(nombre_grupo, descripcion, privacidad) VALUES(%s, %s, %s)"
        cursor.execute(sql, (nombre_grupo, descripcion, privacidad))
        grupo_id = cursor.lastrowid  # Obtener el ID del grupo recién creado

        sql_miembro = "INSERT INTO miembros(grupo_id, usuario_id, rol) VALUES(%s, %s, 'Administrador')"
        cursor.execute(sql_miembro, (grupo_id, usuario_id))

        connex.commit()
        return "Grupo creado exitosamente y usuario añadido como miembro."
    except Error as e:
        return f"Error al crear grupo: {e}"
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()

# Función para actualizar perfil
def actualizar_perfil(id, nuevo_nombre, nuevo_apellido, nuevo_fecha_nacimiento, nuevo_genero, nuevo_correo_electronico, nuevo_contraseña):
    connex = conexion()
    cursor = connex.cursor()
    try:
        campos_actualizar = []
        valores_actualizar = []

        if nuevo_nombre:
            campos_actualizar.append("nombre = %s")
            valores_actualizar.append(nuevo_nombre)
        if nuevo_apellido:
            campos_actualizar.append("apellido = %s")
            valores_actualizar.append(nuevo_apellido)
        if nuevo_fecha_nacimiento:
            campos_actualizar.append("fecha_nacimiento = %s")
            valores_actualizar.append(nuevo_fecha_nacimiento)
        if nuevo_genero:
            campos_actualizar.append("genero = %s")
            valores_actualizar.append(nuevo_genero)
        if nuevo_correo_electronico:
            campos_actualizar.append("correo_electronico = %s")
            valores_actualizar.append(nuevo_correo_electronico)
        if nuevo_contraseña:
            salt = bcrypt.gensalt()
            contraseña_hash = bcrypt.hashpw(nuevo_contraseña.encode('utf-8'), salt)
            campos_actualizar.append("contraseña = %s")
            valores_actualizar.append(contraseña_hash)

        valores_actualizar.append(id)
        sql = f"UPDATE perfil SET {', '.join(campos_actualizar)} WHERE id = %s"
        cursor.execute(sql, valores_actualizar)
        connex.commit()
        return "Perfil actualizado de manera exitosa"
    except Error as e:
        return f"Error al actualizar el perfil: {e}"
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()

# Función para actualizar publicación
def actualizar_publicacion(id, nuevo_titulo, nuevo_contenido):
    connex = conexion()
    cursor = connex.cursor()
    try:
        campos_actualizar = []
        valores_actualizar = []
        if nuevo_titulo:
            campos_actualizar.append("titulo_publicacion = %s")
            valores_actualizar.append(nuevo_titulo)
        if nuevo_contenido:
            campos_actualizar.append("contenido = %s")
            valores_actualizar.append(nuevo_contenido)
        
        valores_actualizar.append(id)
        sql = f"UPDATE publicacion SET {', '.join(campos_actualizar)} WHERE id = %s"
        cursor.execute(sql, valores_actualizar)
        connex.commit()
        return "Publicación actualizada exitosamente"
    except Error as e:
        return f"Error al actualizar la publicación: {e}"
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()

# Función para actualizar grupo
def actualizar_grupo(id, nuevo_nombre_grupo, nueva_descripcion, nueva_privacidad):
    connex = conexion()
    cursor = connex.cursor()
    try:
        campos_actualizar = []
        valores_actualizar = []

        if nuevo_nombre_grupo:
            campos_actualizar.append("nombre_grupo = %s")
            valores_actualizar.append(nuevo_nombre_grupo)
        if nueva_descripcion:
            campos_actualizar.append("descripcion = %s")
            valores_actualizar.append(nueva_descripcion)
        if nueva_privacidad:
            campos_actualizar.append("privacidad = %s")
            valores_actualizar.append(nueva_privacidad)
        
        valores_actualizar.append(id)
        sql = f"UPDATE grupo SET {', '.join(campos_actualizar)} WHERE id = %s"
        cursor.execute(sql, valores_actualizar)
        connex.commit()
        return "Grupo actualizado exitosamente."
    except Error as e:
        return f"Error al actualizar grupo: {e}"
    finally:
        if connex.is_connected():
            cursor.close()
            connex.close()
