from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random
import threading
import pyttsx3

# ------------------------------
# Voice Engine Setup
# ------------------------------
voice_engine = pyttsx3.init()
voice_lock = threading.Lock()

def speak_async(text: str):
    def run():
        with voice_lock:
            voice_engine.say(text)
            voice_engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# ------------------------------
# FastAPI App Setup
# ------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows requests from any frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Models
# ------------------------------
class AppointmentRequest(BaseModel):
    service_type: str
    preferred_date: str  # YYYY-MM-DD
    time_range: Optional[str] = "any"  # morning/afternoon/evening
    user_name: Optional[str] = "Guest"

# ------------------------------
# Simulated Provider Data
# ------------------------------
providers = [
    {"id": 1, "name": "Smile Dental Clinic", "type": "dentist", "rating": 4.8, "distance_km": 3},
    {"id": 2, "name": "Happy Teeth Dental", "type": "dentist", "rating": 4.5, "distance_km": 7},
    {"id": 3, "name": "City Health Clinic", "type": "general", "rating": 4.3, "distance_km": 5},
    {"id": 4, "name": "Downtown Car Repair", "type": "car", "rating": 4.6, "distance_km": 4},
    {"id": 5, "name": "Premium Hair Salon", "type": "hair", "rating": 4.9, "distance_km": 6},
]

# ------------------------------
# Helper Functions
# ------------------------------
def generate_available_slots(date_str, time_range="any"):
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    slots = []

    if time_range == "morning":
        hours = range(9, 12)
    elif time_range == "afternoon":
        hours = range(12, 17)
    elif time_range == "evening":
        hours = range(17, 19)
    else:
        hours = range(9, 18)

    for i in hours:
        slots.append(f"{base_date.date()} {i}:00")

    random.shuffle(slots)
    return slots[:5]

def choose_best_providers(service_type, preferred_date, time_range="any"):
    candidates = [p.copy() for p in providers if p["type"] == service_type]
    if not candidates:
        return []

    for p in candidates:
        p["score"] = p["rating"] * 2 - p["distance_km"]
        available_slots = generate_available_slots(preferred_date, time_range)
        p["appointment_slot"] = available_slots[0] if available_slots else "N/A"

    top_providers = sorted(candidates, key=lambda x: x["score"], reverse=True)[:3]
    return top_providers

# ------------------------------
# API Endpoints
# ------------------------------
@app.get("/")
def read_root():
    return {"message": "CallPilot backend is running!"}

@app.get("/get_providers")
def get_providers():
    return {"providers": providers}

@app.post("/request_appointment")
def request_appointment(req: AppointmentRequest):
    return {"message": "Appointment request received", "request": req.dict()}

@app.post("/book_appointment")
def book_appointment(req: AppointmentRequest):
    top_providers = choose_best_providers(req.service_type, req.preferred_date, req.time_range)
    
    if not top_providers:
        return {"message": "No provider found for this service type."}

    # Best provider for confirmation
    best = top_providers[0]
    confirmation = {
        "provider_name": best["name"],
        "service_type": best["type"],
        "appointment_slot": best["appointment_slot"],
        "provider_rating": best["rating"],
        "provider_distance_km": best["distance_km"],
    }

    # -----------------------
    # Voice output for all top 3 providers
    # -----------------------
    for idx, p in enumerate(top_providers, start=1):
        speech_text = (
            f"Option {idx}: {p['name']} for {p['type']} at {p['appointment_slot']}, "
            f"rating {p['rating']} stars, distance {p['distance_km']} kilometers."
        )
        speak_async(speech_text)

    # Also announce confirmation for best provider
    confirm_text = (
        f"Your appointment with {confirmation['provider_name']} for {confirmation['service_type']} "
        f"has been booked at {confirmation['appointment_slot']}."
    )
    speak_async(confirm_text)

    return {
        "message": "Appointment booked successfully!",
        "confirmation": confirmation,
        "top_providers": top_providers
    }
