from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# =========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =========================================================
USER = "root"
PASSWORD = ""
HOST = "localhost"
PORT = "3306"
DATABASE = "taskly_db"

# =========================================================
# URL DE CONEXIÓN PARA MYSQL CON PYMysql
# =========================================================
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# =========================================================
# MOTOR DE CONEXIÓN
# =========================================================
engine = create_engine(
    DATABASE_URL,
    echo=True  # Cambia a False cuando ya no quieras ver consultas en consola
)

# =========================================================
# SESIONES
# =========================================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================================================
# DEPENDENCIA PARA FASTAPI
# =========================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()