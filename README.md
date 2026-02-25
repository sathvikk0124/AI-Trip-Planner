# 🚉🚗 AI Trip Planner ✈️🚌

An intelligent travel itinerary generator built using **Streamlit** and **Google Gemini AI**.

[ **Live Demo**](https://aitripplanner1.streamlit.app/)

##  This web app allows users to:

-  **Create an account & login securely**  
-  **Plan trips based on destination, budget, duration & interests**  
-  **Generate AI-powered personalized itineraries**  
-  **Save and manage previous trip plans**  
-  **Enjoy a modern UI with a dynamic background**  

##  How It Works

### The app uses:

- **Streamlit** for frontend and app logic  
- **SQLite** for user authentication and trip storage  
- **bcrypt** for secure password hashing  
- **Google Gemini AI (via API)** for itinerary generation  

### The AI creates structured, multi-day travel plans including:

- Daily schedules  
- Travel tips  
- Budget suggestions  
- Recommendations based on user interests  


##  Setup Instructions (Important)

### This app requires a Google Gemini API key to generate AI itineraries.

### The API key is **NOT included** in this repository for security reasons.


##  Step 1: Get a Free Gemini API Key

1. Go to [AI Studio](https://aistudio.google.com)  
2. Sign in with your Google account  
3. Click **"Get API key"**  
4. Create a new API key  
5. Copy the generated key  


##  Step 2: Add the API Key to Streamlit Cloud

### If deploying on Streamlit Community Cloud:

1. Open your deployed app  
2. Click **“Manage App”** (bottom right corner)  
3. Go to **Settings → Secrets**  
4. Add the following:

GOOGLE_API_KEY = "your_actual_api_key_here"

> Replace `"your_actual_api_key_here"` with your actual key.

5. Click **Save**  
6. Click **Reboot App**  

## Step 3: Done

Once the secret is added:

- The warning message will disappear  
- AI itinerary generation will work  
- The app is fully functional  

## 🗂 Project Structure

ai-trip-planner/
│
├── app.py
├── background.png
├── requirements.txt
└── README.md


## 🔒 Security Note

- API key is stored securely using Streamlit Secrets  
- It is **NOT visible** in the repository  
- It is **NOT accessible** to public users  
- Passwords are securely hashed using bcrypt  

## ⚠️ Important Note About Database

- This project uses **SQLite**  
- On Streamlit Cloud, data may reset on redeployment  
- Suitable for demo and portfolio projects  
- Not intended for large-scale production use  

## 🚀 Features

- User Authentication (Login / Signup / Reset Password)  
- AI Trip Generation  
- Trip History Management  
- Clean UI with Custom Styling  
- Cloud Deployment Ready 
