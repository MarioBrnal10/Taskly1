from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from DB.conexion import SessionLocal
from models.modelsDB import Prioridad

routerPrioridades = APIRouter()


# -------------------------------------------------
# 🔹 GET - Obtener todas las prioridades
# -------------------------------------------------
@routerPrioridades.get('/prioridades', tags=['Prioridades'])
def obtener_prioridades():
    session = SessionLocal()
    try:
        prioridades = session.query(Prioridad).filter(Prioridad.eliminado == 0).all()

        resultado = []
        for prioridad in prioridades:
            resultado.append({
                "id_prioridad": prioridad.id_prioridad,
                "nombre": prioridad.nombre,
                "color_hex": prioridad.color_hex,
                "creado_en": str(prioridad.creado_en) if prioridad.creado_en else None,
                "actualizado_en": str(prioridad.actualizado_en) if prioridad.actualizado_en else None
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()