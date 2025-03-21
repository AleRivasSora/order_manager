from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/order_manager_db"


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