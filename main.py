from fastapi import FastAPI
from routers.usuarios import routerUsuarios
from routers.materias import routerMaterias
from routers.tareas import routerTareas
from routers.prioridades import routerPrioridades
app = FastAPI(
    title="API Taskly",
    version="1.0"

)

@app.get("/", tags=["Inicio"])
def inicio():
    return {"message": "API Taskly funcionando correctamente"}

app.include_router(routerUsuarios)
app.include_router(routerMaterias)
app.include_router(routerTareas)
app.include_router(routerPrioridades)

