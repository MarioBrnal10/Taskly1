from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime, date

from DB.conexion import SessionLocal
from models.modelsDB import Tarea, Materia, Prioridad, Usuario
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

# -------------------------------------------------
# 🔹 GET - Obtener tareas por usuario
# -------------------------------------------------
@routerTareas.get('/usuarios/{id_usuario}/tareas', tags=['Tareas'])
def obtener_tareas_por_usuario(id_usuario: int):
    session = SessionLocal()
    try:
        materias = session.query(Materia).filter(
            Materia.id_usuario == id_usuario,
            Materia.eliminado == 0
        ).all()

        if not materias:
            return JSONResponse(content=[])

        ids_materias = [materia.id_materia for materia in materias]

        tareas = session.query(Tarea).filter(
            Tarea.id_materia.in_(ids_materias),
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# -------------------------------------------------
# 🔹 GET - Obtener resumen del dashboard por usuario
# -------------------------------------------------
@routerTareas.get('/usuarios/{id_usuario}/dashboard', tags=['Tareas'])
def obtener_dashboard_por_usuario(id_usuario: int):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(
            Usuario.id_usuario == id_usuario,
            Usuario.eliminado == 0
        ).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        materias = session.query(Materia).filter(
            Materia.id_usuario == id_usuario,
            Materia.eliminado == 0
        ).all()

        ids_materias = [materia.id_materia for materia in materias]

        tareas = []
        if ids_materias:
            tareas = session.query(Tarea).filter(
                Tarea.id_materia.in_(ids_materias),
                Tarea.eliminado == 0
            ).all()

        hoy = date.today()

        tareas_pendientes = [t for t in tareas if t.estado == "pendiente"]
        tareas_completadas = [t for t in tareas if t.estado == "completada"]
        tareas_vencen_hoy = [
            t for t in tareas
            if t.estado == "pendiente" and t.fecha_entrega == hoy
        ]

        materias_resumen = []
        for materia in materias:
            tareas_materia = [t for t in tareas if t.id_materia == materia.id_materia]
            materias_resumen.append({
                "id_materia": materia.id_materia,
                "nombre": materia.nombre,
                "descripcion": materia.descripcion,
                "color_hex": materia.color_hex,
                "total_tareas": len(tareas_materia),
                "pendientes": len([t for t in tareas_materia if t.estado == "pendiente"]),
                "completadas": len([t for t in tareas_materia if t.estado == "completada"])
            })

        proximas_tareas = sorted(
            [t for t in tareas if t.estado == "pendiente" and t.fecha_entrega is not None],
            key=lambda x: (x.fecha_entrega, x.hora_entrega if x.hora_entrega else datetime.min.time())
        )[:5]

        proximas_tareas_resultado = []
        for tarea in proximas_tareas:
            proximas_tareas_resultado.append({
                "id_tarea": tarea.id_tarea,
                "id_materia": tarea.id_materia,
                "id_prioridad": tarea.id_prioridad,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "fecha_entrega": str(tarea.fecha_entrega) if tarea.fecha_entrega else None,
                "hora_entrega": str(tarea.hora_entrega) if tarea.hora_entrega else None,
                "estado": tarea.estado
            })

        return JSONResponse(content={
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "total_materias": len(materias),
            "tareas_pendientes": len(tareas_pendientes),
            "tareas_completadas": len(tareas_completadas),
            "tareas_vencen_hoy": len(tareas_vencen_hoy),
            "materias": materias_resumen,
            "proximas_tareas": proximas_tareas_resultado
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# -------------------------------------------------
# 🔹 GET - Obtener tareas que vencen hoy por usuario
# -------------------------------------------------
@routerTareas.get('/usuarios/{id_usuario}/tareas/hoy', tags=['Tareas'])
def obtener_tareas_hoy_por_usuario(id_usuario: int):
    session = SessionLocal()
    try:
        materias = session.query(Materia).filter(
            Materia.id_usuario == id_usuario,
            Materia.eliminado == 0
        ).all()

        if not materias:
            return JSONResponse(content=[])

        ids_materias = [materia.id_materia for materia in materias]
        hoy = date.today()

        tareas = session.query(Tarea).filter(
            Tarea.id_materia.in_(ids_materias),
            Tarea.fecha_entrega == hoy,
            Tarea.estado == "pendiente",
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
                "estado": tarea.estado
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# -------------------------------------------------
# 🔹 GET - Obtener tareas pendientes por usuario
# -------------------------------------------------
@routerTareas.get('/usuarios/{id_usuario}/tareas/pendientes', tags=['Tareas'])
def obtener_tareas_pendientes_por_usuario(id_usuario: int):
    session = SessionLocal()
    try:
        materias = session.query(Materia).filter(
            Materia.id_usuario == id_usuario,
            Materia.eliminado == 0
        ).all()

        if not materias:
            return JSONResponse(content=[])

        ids_materias = [materia.id_materia for materia in materias]

        tareas = session.query(Tarea).filter(
            Tarea.id_materia.in_(ids_materias),
            Tarea.estado == "pendiente",
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
                "estado": tarea.estado
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# -------------------------------------------------
# 🔹 GET - Obtener tareas completadas por usuario
# -------------------------------------------------
@routerTareas.get('/usuarios/{id_usuario}/tareas/completadas', tags=['Tareas'])
def obtener_tareas_completadas_por_usuario(id_usuario: int):
    session = SessionLocal()
    try:
        materias = session.query(Materia).filter(
            Materia.id_usuario == id_usuario,
            Materia.eliminado == 0
        ).all()

        if not materias:
            return JSONResponse(content=[])

        ids_materias = [materia.id_materia for materia in materias]

        tareas = session.query(Tarea).filter(
            Tarea.id_materia.in_(ids_materias),
            Tarea.estado == "completada",
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
                "estado": tarea.estado
            })

        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()