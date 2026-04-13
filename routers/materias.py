from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

from DB.conexion import SessionLocal
from models.modelsDB import Materia, Usuario
from modelsPydantic import modeloMateria

routerMaterias = APIRouter()


# -------------------------------------------------
# 🔹 GET - Obtener todas las materias
# -------------------------------------------------
@routerMaterias.get('/materias', tags=['Materias'])
def obtener_materias():
    session = SessionLocal()
    try:
        materias = session.query(Materia).filter(Materia.eliminado == 0).all()

        resultado = []
        for materia in materias:
            resultado.append({
                "id_materia": materia.id_materia,
                "id_usuario": materia.id_usuario,
                "nombre": materia.nombre,
                "descripcion": materia.descripcion,
                "color_hex": materia.color_hex,
                "creado_en": str(materia.creado_en) if materia.creado_en else None,
                "actualizado_en": str(materia.actualizado_en) if materia.actualizado_en else None
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 GET - Obtener una materia por ID
# -------------------------------------------------
@routerMaterias.get('/materias/{id}', tags=['Materias'])
def obtener_materia(id: int):
    session = SessionLocal()
    try:
        materia = session.query(Materia).filter(
            Materia.id_materia == id,
            Materia.eliminado == 0
        ).first()

        if not materia:
            raise HTTPException(status_code=404, detail="Materia no encontrada")

        return JSONResponse(content={
            "id_materia": materia.id_materia,
            "id_usuario": materia.id_usuario,
            "nombre": materia.nombre,
            "descripcion": materia.descripcion,
            "color_hex": materia.color_hex,
            "creado_en": str(materia.creado_en) if materia.creado_en else None,
            "actualizado_en": str(materia.actualizado_en) if materia.actualizado_en else None
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 POST - Crear una nueva materia
# -------------------------------------------------
@routerMaterias.post('/materias', tags=['Materias'])
def crear_materia(materia: modeloMateria):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == materia.id_usuario,
            Usuario.eliminado == 0
        ).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        nueva_materia = Materia(
            id_usuario=materia.id_usuario,
            nombre=materia.nombre,
            descripcion=materia.descripcion,
            color_hex=materia.color_hex,
            creado_en=datetime.now(),
            actualizado_en=datetime.now(),
            eliminado=0
        )

        session.add(nueva_materia)
        session.commit()

        return JSONResponse(content={"message": "Materia creada exitosamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 PUT - Editar una materia por ID
# -------------------------------------------------
@routerMaterias.put('/materias/{id}', tags=['Materias'])
def actualizar_materia(id: int, materia: modeloMateria):
    session = SessionLocal()
    try:
        materia_db = session.query(Materia).filter(
            Materia.id_materia == id,
            Materia.eliminado == 0
        ).first()

        if not materia_db:
            raise HTTPException(status_code=404, detail="Materia no encontrada")

        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == materia.id_usuario,
            Usuario.eliminado == 0
        ).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        materia_db.id_usuario = materia.id_usuario
        materia_db.nombre = materia.nombre
        materia_db.descripcion = materia.descripcion
        materia_db.color_hex = materia.color_hex
        materia_db.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Materia actualizada exitosamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 DELETE - Eliminación lógica de materia por ID
# -------------------------------------------------
@routerMaterias.delete('/materias/{id}', tags=['Materias'])
def eliminar_materia(id: int):
    session = SessionLocal()
    try:
        materia = session.query(Materia).filter(
            Materia.id_materia == id,
            Materia.eliminado == 0
        ).first()

        if not materia:
            raise HTTPException(status_code=404, detail="Materia no encontrada")

        materia.eliminado = 1
        materia.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Materia eliminada correctamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()