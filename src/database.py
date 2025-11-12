"""
Simple Database configuration for Mergington High School API
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL - SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mergington_activities.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    activity = relationship("Activity")
    user = relationship("User")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def init_sample_data():
    """Initialize the database with sample activity data"""
    db = SessionLocal()
    
    # Check if activities already exist
    if db.query(Activity).count() > 0:
        db.close()
        return
    
    # Sample activities data
    sample_activities = [
        Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
        Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
        Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
        Activity(name="Soccer Team", description="Join the school soccer team and compete in matches", schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM", max_participants=22),
        Activity(name="Basketball Team", description="Practice and play basketball with the school team", schedule="Wednesdays and Fridays, 3:30 PM - 5:00 PM", max_participants=15),
        Activity(name="Art Club", description="Explore your creativity through painting and drawing", schedule="Thursdays, 3:30 PM - 5:00 PM", max_participants=15),
        Activity(name="Drama Club", description="Act, direct, and produce plays and performances", schedule="Mondays and Wednesdays, 4:00 PM - 5:30 PM", max_participants=20),
        Activity(name="Math Club", description="Solve challenging problems and participate in math competitions", schedule="Tuesdays, 3:30 PM - 4:30 PM", max_participants=10),
        Activity(name="Debate Team", description="Develop public speaking and argumentation skills", schedule="Fridays, 4:00 PM - 5:30 PM", max_participants=12)
    ]
    
    # Sample users with existing registrations
    sample_users = [
        User(email="michael@mergington.edu", name="Michael"),
        User(email="daniel@mergington.edu", name="Daniel"),
        User(email="emma@mergington.edu", name="Emma"),
        User(email="sophia@mergington.edu", name="Sophia"),
        User(email="john@mergington.edu", name="John"),
        User(email="olivia@mergington.edu", name="Olivia"),
        User(email="liam@mergington.edu", name="Liam"),
        User(email="noah@mergington.edu", name="Noah"),
        User(email="ava@mergington.edu", name="Ava"),
        User(email="mia@mergington.edu", name="Mia"),
        User(email="amelia@mergington.edu", name="Amelia"),
        User(email="harper@mergington.edu", name="Harper"),
        User(email="ella@mergington.edu", name="Ella"),
        User(email="scarlett@mergington.edu", name="Scarlett"),
        User(email="james@mergington.edu", name="James"),
        User(email="benjamin@mergington.edu", name="Benjamin"),
        User(email="charlotte@mergington.edu", name="Charlotte"),
        User(email="henry@mergington.edu", name="Henry")
    ]
    
    # Add activities and users
    db.add_all(sample_activities)
    db.add_all(sample_users)
    db.commit()
    
    # Create participant relationships to match original data
    participants = [
        Participant(activity_id=1, user_id=1),  # Michael -> Chess Club
        Participant(activity_id=1, user_id=2),  # Daniel -> Chess Club
        Participant(activity_id=2, user_id=3),  # Emma -> Programming Class
        Participant(activity_id=2, user_id=4),  # Sophia -> Programming Class
        Participant(activity_id=3, user_id=5),  # John -> Gym Class
        Participant(activity_id=3, user_id=6),  # Olivia -> Gym Class
        Participant(activity_id=4, user_id=7),  # Liam -> Soccer Team
        Participant(activity_id=4, user_id=8),  # Noah -> Soccer Team
        Participant(activity_id=5, user_id=9),  # Ava -> Basketball Team
        Participant(activity_id=5, user_id=10), # Mia -> Basketball Team
        Participant(activity_id=6, user_id=11), # Amelia -> Art Club
        Participant(activity_id=6, user_id=12), # Harper -> Art Club
        Participant(activity_id=7, user_id=13), # Ella -> Drama Club
        Participant(activity_id=7, user_id=14), # Scarlett -> Drama Club
        Participant(activity_id=8, user_id=15), # James -> Math Club
        Participant(activity_id=8, user_id=16), # Benjamin -> Math Club
        Participant(activity_id=9, user_id=17), # Charlotte -> Debate Team
        Participant(activity_id=9, user_id=18), # Henry -> Debate Team
    ]
    
    db.add_all(participants)
    db.commit()
    db.close()