from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from DB.base import Base


# modelo usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    creado_en = Column(DateTime)
    actualizado_en = Column(DateTime)
    eliminado = Column(Integer, default=0, nullable=False)

    materias = relationship("Materia", back_populates="usuario")


# modelo prioridad
class Prioridad(Base):
    __tablename__ = 'prioridades'

    id_prioridad = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), unique=True, nullable=False)
    color_hex = Column(String(10), nullable=True)
    creado_en = Column(DateTime)
    actualizado_en = Column(DateTime)
    eliminado = Column(Integer, default=0, nullable=False)

    tareas = relationship("Tarea", back_populates="prioridad")


# modelo materia
class Materia(Base):
    __tablename__ = 'materias'

    id_materia = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    color_hex = Column(String(10), nullable=True)
    creado_en = Column(DateTime)
    actualizado_en = Column(DateTime)
    eliminado = Column(Integer, default=0, nullable=False)

    usuario = relationship("Usuario", back_populates="materias")
    tareas = relationship("Tarea", back_populates="materia")


# modelo tarea
class Tarea(Base):
    __tablename__ = 'tareas'

    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, ForeignKey('materias.id_materia'), nullable=False)
    id_prioridad = Column(Integer, ForeignKey('prioridades.id_prioridad'), nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_entrega = Column(Date, nullable=True)
    hora_entrega = Column(Time, nullable=True)
    estado = Column(Enum('pendiente', 'completada', name='estado_tarea'), nullable=False, default='pendiente')
    creado_en = Column(DateTime)
    actualizado_en = Column(DateTime)
    eliminado = Column(Integer, default=0, nullable=False)

    materia = relationship("Materia", back_populates="tareas")
    prioridad = relationship("Prioridad", back_populates="tareas")