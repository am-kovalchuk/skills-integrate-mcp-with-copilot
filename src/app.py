"""
High School Management System API

A FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
Now with persistent database storage!
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import os
from pathlib import Path

# Import database components
from .database import get_db, create_tables, init_sample_data, Activity, User, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    create_tables()
    init_sample_data()

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities with their participants"""
    activities_list = db.query(Activity).all()
    
    # Convert to the format expected by the frontend
    activities_dict = {}
    for activity in activities_list:
        # Get participants for this activity
        participants = db.query(Participant).filter(Participant.activity_id == activity.id).all()
        participant_emails = []
        for participant in participants:
            user = db.query(User).filter(User.id == participant.user_id).first()
            if user:
                participant_emails.append(user.email)
        
        activities_dict[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": participant_emails
        }
    
    return activities_dict


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Find the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if activity is full
    participant_count = db.query(Participant).filter(Participant.activity_id == activity.id).count()
    if participant_count >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Find or create user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Extract name from email (simple approach)
        name = email.split('@')[0].title()
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Check if user is already signed up
    existing_participant = db.query(Participant).filter(
        Participant.activity_id == activity.id,
        Participant.user_id == user.id
    ).first()
    
    if existing_participant:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add user to activity
    participant = Participant(activity_id=activity.id, user_id=user.id)
    db.add(participant)
    db.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Find the activity
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find the participant record
    participant = db.query(Participant).filter(
        Participant.activity_id == activity.id,
        Participant.user_id == user.id
    ).first()
    
    if not participant:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove participant record
    db.delete(participant)
    db.commit()
    
    return {"message": f"Unregistered {email} from {activity_name}"}
