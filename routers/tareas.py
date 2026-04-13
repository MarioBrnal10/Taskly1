from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime

from DB.conexion import SessionLocal
from models.modelsDB import Tarea, Materia, Prioridad
from modelsPydantic import modeloTarea

routerTareas = APIRouter()


# -------------------------------------------------
# 🔹 GET - Obtener todas las tareas
# -------------------------------------------------
@routerTareas.get('/tareas', tags=['Tareas'])
def obtener_tareas():
    session = SessionLocal()
    try:
        tareas = session.query(Tarea).filter(Tarea.eliminado == 0).all()

        resultado = []
        for tarea in tareas:
            resultado.append({
                "id_tarea": tarea.id_tarea,
                "id_materia": tarea.id_materia,
                "id_prioridad": tarea.id_prioridad,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "fecha_entrega": str(tarea.fecha_entrega) if tarea.fecha_entrega else None,
                "hora_entrega": str(tarea.hora_entrega) if tarea.hora_entrega else None,
                "estado": tarea.estado,
                "creado_en": str(tarea.creado_en) if tarea.creado_en else None,
                "actualizado_en": str(tarea.actualizado_en) if tarea.actualizado_en else None
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 GET - Obtener una tarea por ID
# -------------------------------------------------
@routerTareas.get('/tareas/{id}', tags=['Tareas'])
def obtener_tarea(id: int):
    session = SessionLocal()
    try:
        tarea = session.query(Tarea).filter(
            Tarea.id_tarea == id,
            Tarea.eliminado == 0
        ).first()

        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        return JSONResponse(content={
            "id_tarea": tarea.id_tarea,
            "id_materia": tarea.id_materia,
            "id_prioridad": tarea.id_prioridad,
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "fecha_entrega": str(tarea.fecha_entrega) if tarea.fecha_entrega else None,
            "hora_entrega": str(tarea.hora_entrega) if tarea.hora_entrega else None,
            "estado": tarea.estado,
            "creado_en": str(tarea.creado_en) if tarea.creado_en else None,
            "actualizado_en": str(tarea.actualizado_en) if tarea.actualizado_en else None
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 POST - Crear una nueva tarea
# -------------------------------------------------
@routerTareas.post('/tareas', tags=['Tareas'])
def crear_tarea(tarea: modeloTarea):
    session = SessionLocal()
    try:
        materia = session.query(Materia).filter(
            Materia.id_materia == tarea.id_materia,
            Materia.eliminado == 0
        ).first()

        if not materia:
            raise HTTPException(status_code=404, detail="La materia no existe")

        prioridad = session.query(Prioridad).filter(
            Prioridad.id_prioridad == tarea.id_prioridad,
            Prioridad.eliminado == 0
        ).first()

        if not prioridad:
            raise HTTPException(status_code=404, detail="La prioridad no existe")

        nueva_tarea = Tarea(
            id_materia=tarea.id_materia,
            id_prioridad=tarea.id_prioridad,
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            fecha_entrega=tarea.fecha_entrega,
            hora_entrega=tarea.hora_entrega,
            estado=tarea.estado,
            creado_en=datetime.now(),
            actualizado_en=datetime.now(),
            eliminado=0
        )

        session.add(nueva_tarea)
        session.commit()

        return JSONResponse(content={"message": "Tarea creada exitosamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 PUT - Editar una tarea por ID
# -------------------------------------------------
@routerTareas.put('/tareas/{id}', tags=['Tareas'])
def actualizar_tarea(id: int, tarea: modeloTarea):
    session = SessionLocal()
    try:
        tarea_db = session.query(Tarea).filter(
            Tarea.id_tarea == id,
            Tarea.eliminado == 0
        ).first()

        if not tarea_db:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        materia = session.query(Materia).filter(
            Materia.id_materia == tarea.id_materia,
            Materia.eliminado == 0
        ).first()

        if not materia:
            raise HTTPException(status_code=404, detail="La materia no existe")

        prioridad = session.query(Prioridad).filter(
            Prioridad.id_prioridad == tarea.id_prioridad,
            Prioridad.eliminado == 0
        ).first()

        if not prioridad:
            raise HTTPException(status_code=404, detail="La prioridad no existe")

        tarea_db.id_materia = tarea.id_materia
        tarea_db.id_prioridad = tarea.id_prioridad
        tarea_db.titulo = tarea.titulo
        tarea_db.descripcion = tarea.descripcion
        tarea_db.fecha_entrega = tarea.fecha_entrega
        tarea_db.hora_entrega = tarea.hora_entrega
        tarea_db.estado = tarea.estado
        tarea_db.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Tarea actualizada exitosamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 DELETE - Eliminación lógica de tarea por ID
# -------------------------------------------------
@routerTareas.delete('/tareas/{id}', tags=['Tareas'])
def eliminar_tarea(id: int):
    session = SessionLocal()
    try:
        tarea = session.query(Tarea).filter(
            Tarea.id_tarea == id,
            Tarea.eliminado == 0
        ).first()

        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        tarea.eliminado = 1
        tarea.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Tarea eliminada correctamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 PUT - Marcar tarea como completada
# -------------------------------------------------
@routerTareas.put('/tareas/{id}/completar', tags=['Tareas'])
def completar_tarea(id: int):
    session = SessionLocal()
    try:
        tarea = session.query(Tarea).filter(
            Tarea.id_tarea == id,
            Tarea.eliminado == 0
        ).first()

        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        tarea.estado = "completada"
        tarea.actualizado_en = datetime.now()

        session.commit()

        return JSONResponse(content={"message": "Tarea marcada como completada"})
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 GET - Obtener tareas por materia
# -------------------------------------------------
@routerTareas.get('/tareas/materia/{id_materia}', tags=['Tareas'])
def obtener_tareas_por_materia(id_materia: int):
    session = SessionLocal()
    try:
        materia = session.query(Materia).filter(
            Materia.id_materia == id_materia,
            Materia.eliminado == 0
        ).first()

        if not materia:
            raise HTTPException(status_code=404, detail="Materia no encontrada")

        tareas = session.query(Tarea).filter(
            Tarea.id_materia == id_materia,
            Tarea.eliminado == 0
        ).all()

        resultado = []
        for tarea in tareas:
            resultado.append({
                "id_tarea": tarea.id_tarea,
                "id_materia": tarea.id_materia,
                "id_prioridad": tarea.id_prioridad,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "fecha_entrega": str(tarea.fecha_entrega) if tarea.fecha_entrega else None,
                "hora_entrega": str(tarea.hora_entrega) if tarea.hora_entrega else None,
                "estado": tarea.estado,
                "creado_en": str(tarea.creado_en) if tarea.creado_en else None,
                "actualizado_en": str(tarea.actualizado_en) if tarea.actualizado_en else None
            })

        return JSONResponse(content=resultado)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


# -------------------------------------------------
# 🔹 GET - Filtrar tareas por estado o prioridad
# -------------------------------------------------
@routerTareas.get('/tareas/filtro', tags=['Tareas'])
def filtrar_tareas(
    estado: str = Query(None),
    id_prioridad: int = Query(None)
):
    session = SessionLocal()
    try:
        query = session.query(Tarea).filter(Tarea.eliminado == 0)

        if estado:
            query = query.filter(Tarea.estado == estado)

        if id_prioridad:
            query = query.filter(Tarea.id_prioridad == id_prioridad)

        tareas = query.all()

        resultado = []
        for tarea in tareas:
            resultado.append({
                "id_tarea": tarea.id_tarea,
                "id_materia": tarea.id_materia,
                "id_prioridad": tarea.id_prioridad,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "fecha_entrega": str(tarea.fecha_entrega) if tarea.fecha_entrega else None,
                "hora_entrega": str(tarea.hora_entrega) if tarea.hora_entrega else None,
                "estado": tarea.estado,
                "creado_en": str(tarea.creado_en) if tarea.creado_en else None,
                "actualizado_en": str(tarea.actualizado_en) if tarea.actualizado_en else None
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()