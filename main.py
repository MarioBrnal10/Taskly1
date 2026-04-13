from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.usuarios import routerUsuarios
from routers.materias import routerMaterias
from routers.tareas import routerTareas
from routers.prioridades import routerPrioridades

app = FastAPI(
    title="API Taskly",
    version="1.0"
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Inicio"])
def inicio():
    return {"message": "API Taskly funcionando correctamente"}

app.include_router(routerUsuarios)
app.include_router(routerMaterias)
app.include_router(routerTareas)
app.include_router(routerPrioridades)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)