from database import db

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Enum('Masculino', 'Femenino', 'Otro'), nullable=False)
    correo_electronico = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    foto_perfil = db.Column(db.String(255))
    creado = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    # Relación con Publicacion
    publicaciones = db.relationship('Publicacion', backref='perfil', lazy=True)


class Publicacion(db.Model):
    __tablename__ = 'publicacion'
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    creado = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    usuario_id = db.Column(db.Integer, db.ForeignKey('perfil.id'), nullable=False)

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    privacidad = db.Column(db.Enum('Publica', 'Privada', 'Secreta'), nullable=False)
    creado = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    categoria = db.Column(db.String(50), nullable=False)
    numero_miembros = db.Column(db.Integer, default=0)


