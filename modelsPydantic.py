from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, time, datetime


# =========================================================
# MODELO USUARIO
# =========================================================
class modeloUsuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=6, max_length=255, description="Contraseña del usuario")

    class Config:
        from_attributes = True


# =========================================================
# MODELO LOGIN
# =========================================================
class modeloLogin(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., min_length=6, max_length=255, description="Contraseña del usuario")

    class Config:
        from_attributes = True


# =========================================================
# MODELO PRIORIDAD
# =========================================================
class modeloPrioridad(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=45, description="Nombre de la prioridad")
    color_hex: Optional[str] = Field(None, max_length=10, description="Color hexadecimal de la prioridad")

    class Config:
        from_attributes = True


# =========================================================
# MODELO MATERIA
# =========================================================
class modeloMateria(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario propietario de la materia")
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre de la materia")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción de la materia")
    color_hex: Optional[str] = Field(None, max_length=10, description="Color hexadecimal de la materia")

    class Config:
        from_attributes = True


# =========================================================
# MODELO TAREA
# =========================================================
class modeloTarea(BaseModel):
    id_materia: int = Field(..., description="ID de la materia")
    id_prioridad: int = Field(..., description="ID de la prioridad")
    titulo: str = Field(..., min_length=3, max_length=100, description="Título de la tarea")
    descripcion: Optional[str] = Field(None, description="Descripción de la tarea")
    fecha_entrega: Optional[date] = Field(None, description="Fecha de entrega")
    hora_entrega: Optional[time] = Field(None, description="Hora de entrega")
    estado: str = Field("pendiente", description="Estado de la tarea")

    class Config:
        from_attributes = True