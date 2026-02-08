# CallPilot – Agentic Voice AI for Autonomous Appointment Booking 🚀

![Python](https://img.shields.io/badge/Python-FastAPI-green) ![Voice AI](https://img.shields.io/badge/ElevenLabs-VoiceAI-blue) ![Frontend](https://img.shields.io/badge/HTML/CSS/JS-Frontend-yellow)

---

## Overview 💡

**CallPilot** is an AI-powered voice agent that autonomously books appointments for users. It transforms the phone from a **manual bottleneck** into a **programmable execution layer**, eliminating the friction of coordinating schedules across service providers.  

Powered by **ElevenLabs Conversational AI**, CallPilot can:  
- 📞 Call service providers automatically  
- 🤝 Negotiate and select the **best appointment slot** based on user preferences, availability, distance, and ratings  
- 🗣 Provide **voice & text confirmation** to the user  
- ⚡ Support **multiple simultaneous provider calls** (Swarm Mode) for efficiency  

This project demonstrates **next-generation agentic AI** moving beyond conversation to **real-world execution**.

## Features (MVP) ⭐

### Single-Call Appointment Booking
- User requests an appointment via the **web interface**  
- AI agent calls the provider and books a slot  
- **Calendar integration** prevents double-booking  

### Multi-Call Parallel Outreach (Swarm Mode)
- Calls multiple providers simultaneously (up to 15)  
- Aggregates results using a **scoring system** (rating + distance)  
- Returns a **ranked shortlist** for user confirmation  

### Voice & Text Output
- Real-time **voice announcement** of booked appointment  
- **Text summary** displayed in the frontend  

### Time Preference Matching
- Supports **morning, afternoon, evening, or any-time slots**  

## Optional Enhancements / Stretch Goals ✨
- 🌐 Multilingual support with **automatic language detection**  
- 🔄 Rescheduling & cancellation agent  
- 🖥 Live **user-in-the-loop** with transcript streaming  
- ⚠ Hallucination-aware **handover to human** when needed  
- 🩺 Domain expert voice agents (e.g., healthcare scheduling)

## Tech Stack 🛠

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, FastAPI  
- **Voice AI:** ElevenLabs Conversational AI, pyttsx3  
- **External APIs:** Google Calendar, Google Places, Google Maps Distance Matrix  
- **Data Simulation:** JSON for provider database  

## How It Works ⚙️

1. User selects **service type**, **preferred date**, and **time range**.  
2. Frontend sends a **POST request** to the FastAPI backend.  
3. Backend simulates provider availability, scores top providers, and books the best appointment.  
4. AI announces the appointment via **voice** and returns **text confirmation** to the frontend.  
5. Multiple provider options are displayed for **transparency**.


## Usage 🏁

```bash
# Clone the repo
git clone https://github.com/NoorFatima323/callpilot.git
cd callpilot

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn backend.main:app --reload

# Open index.html in your browser and test the agent
```
## Future Work 🚀

Integrate real-world calling via Twilio or SIP

Implement live Google Calendar sync

Add waitlist & callback intelligence

Expand multilingual & domain-specific agents

## Why It Matters 🌟

Appointment booking remains one of the most time-consuming micro-tasks in daily life. CallPilot shows how AI can autonomously negotiate, compare, decide, and act on behalf of users, making the phone as programmable as the internet.

## Author ✍️

Noor Fatima
