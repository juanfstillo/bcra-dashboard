"""
Configuración de la base de datos con SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bcra_dashboard")

# Crear engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    echo=False,  # No mostrar SQL en consola (cambiar a True para debug)
)

# Crear SessionLocal para las transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Dependency para FastAPI que provee una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    """
    from app.models import Variable, DatoBCRA, Usuario  # Importar modelos
    
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente!")


def drop_db():
    """
    CUIDADO: Elimina todas las tablas de la base de datos
    """
    from app.models import Variable, DatoBCRA, Usuario
    
    print("⚠️  ELIMINANDO todas las tablas...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tablas eliminadas!")
