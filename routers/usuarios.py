from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from datetime import datetime
from typing import List

from DB.conexion import SessionLocal
from models.modelsDB import Usuario
from modelsPydantic import modeloUsuario, modeloLogin

routerUsuarios = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------------------------
# 🔹 POST - Inicio de sesión
# -------------------------------------------------
@routerUsuarios.post('/login', tags=['Login'])
def login(usuario: modeloLogin):
    session = SessionLocal()
    try:
        user = session.query(Usuario).filter(
            Usuario.email == usuario.email,
            Usuario.eliminado == 0
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not pwd_context.verify(usuario.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        return JSONResponse(content={
            "message": "Inicio de sesión exitoso",
            "id_usuario": user.id_usuario,
            "nombre": user.nombre,
            "email": user.email
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 GET - Obtener todos los usuarios
# -------------------------------------------------
@routerUsuarios.get('/usuarios', tags=['Usuarios'])
def obtener_usuarios():
    session = SessionLocal()
    try:
        usuarios = session.query(Usuario).filter(Usuario.eliminado == 0).all()

        resultado = []
        for usuario in usuarios:
            resultado.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "creado_en": str(usuario.creado_en) if usuario.creado_en else None,
                "actualizado_en": str(usuario.actualizado_en) if usuario.actualizado_en else None
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 GET - Obtener un usuario por su ID
# -------------------------------------------------
@routerUsuarios.get('/usuarios/{id}', tags=['Usuarios'])
def obtener_usuario(id: int):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == id,
            Usuario.eliminado == 0
        ).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return JSONResponse(content={
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "creado_en": str(usuario.creado_en) if usuario.creado_en else None,
            "actualizado_en": str(usuario.actualizado_en) if usuario.actualizado_en else None
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 POST - Crear un nuevo usuario
# -------------------------------------------------
@routerUsuarios.post('/usuarios', tags=['Usuarios'])
def crear_usuario(usuario: modeloUsuario):
    session = SessionLocal()
    try:
        existente = session.query(Usuario).filter(
            Usuario.email == usuario.email
        ).first()

        if existente and existente.eliminado == 0:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        hashed_password = pwd_context.hash(usuario.password)

        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            password_hash=hashed_password,
            creado_en=datetime.now(),
            actualizado_en=datetime.now(),
            eliminado=0
        )

        session.add(nuevo_usuario)
        session.commit()

        return JSONResponse(content={"message": "Usuario creado exitosamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 PUT - Editar un usuario por ID
# -------------------------------------------------
@routerUsuarios.put('/usuarios/{id}', tags=['Usuarios'])
def actualizar_usuario(id: int, usuario: modeloUsuario):
    session = SessionLocal()
    try:
        user = session.query(Usuario).filter(
            Usuario.id_usuario == id,
            Usuario.eliminado == 0
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        correo_existente = session.query(Usuario).filter(
            Usuario.email == usuario.email,
            Usuario.id_usuario != id,
            Usuario.eliminado == 0
        ).first()

        if correo_existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado por otro usuario")

        user.nombre = usuario.nombre
        user.email = usuario.email
        user.password_hash = pwd_context.hash(usuario.password)
        user.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Usuario actualizado exitosamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 DELETE - Eliminación lógica de usuario por ID
# -------------------------------------------------
@routerUsuarios.delete('/usuarios/{id}', tags=['Usuarios'])
def eliminar_usuario(id: int):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == id,
            Usuario.eliminado == 0
        ).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario.eliminado = 1
        usuario.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Usuario eliminado correctamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()