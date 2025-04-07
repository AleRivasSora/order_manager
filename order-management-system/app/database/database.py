from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/order_manager_db"

Base = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_connection():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

def execute_query(query: str, params: dict = None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        return result.fetchall()
    
def initialize_database():
    """
    Crea las tablas en la base de datos si no existen.
    """
    try:
        import app.models 
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas o ya existentes en la base de datos.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")