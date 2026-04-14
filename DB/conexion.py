from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# =========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =========================================================
USER = "root"
PASSWORD = "RphoSsWuZpHuafsFPoAAaPNvJRSRRMhU"
HOST = "mainline.proxy.rlwy.net"
PORT = "14645"
DATABASE = "railway"

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