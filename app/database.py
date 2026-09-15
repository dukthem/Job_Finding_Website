from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Where the database file will be stored
SQLALCHEMY_DATABASE_URL = "sqlite:///./careerpluse.db"

# The Engine (The connection manager)
engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                        connect_args = {"check_same_thread": False})

# The Session Factory (Spawns a new database session per request)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# The Base class (All our database tables will inherit from this)
Base = declarative_base()

# Database Dependency (Safely opens and closes database connections)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        