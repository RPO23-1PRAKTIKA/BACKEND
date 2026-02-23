from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#sqlalchemy нужен для удобного общения с бд, на питоне

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/company_db"

engine = create_engine( #Сам движок мы туда передаем ссылку на бд, echo вроде нужен для отладки
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker( #Посути это нужно для создания ссесий
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() #Нужно для того, чтобы можно было воссоздать таблицы бд с помощью классов

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()