from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from passlib.context import CryptContext

from sqlalchemy.orm import declarative_base

Base = declarative_base()
# Switching to pbkdf2_sha256 to avoid bcrypt 72 byte limit/encoding issues on Windows
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def setup_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', '..', 'data', 'users.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    return SessionLocal

def get_db():
    SessionLocal = setup_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_users():
    SessionLocal = setup_database()
    db = SessionLocal()
    
    users = [
        ("arshad@rbac.com", "arshad@rbac.com", "admin123", "c-level"),
        ("priyanshu@rbac.com", "priyanshu@rbac.com", "pass123", "finance"),
        ("kanak@rbac.com", "kanak@rbac.com", "pass123", "hr"),
        ("shirisha@rbac.com", "shirisha@rbac.com", "pass123", "marketing"),
        ("eng_user", "eng@company.com", "pass123", "engineering"),
        ("employee", "employee@company.com", "pass123", "employees")
    ]
    
    # Clear existing users to ensure new usernames are applied
    db.query(User).delete()
    db.commit()
    
    for username, email, password, role in users:
        hashed = pwd_context.hash(password)
        user = User(username=username, email=email, hashed_password=hashed, role=role)
        db.add(user)
        print(f"Created user: {username} ({role})")
            
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_users()
