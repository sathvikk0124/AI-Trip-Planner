import streamlit as st
import sqlite3
import bcrypt
import base64
import google.generativeai as genai
from pathlib import Path


# 1. CONFIG & MODELS

st.set_page_config(page_title="AI Trip Planner", page_icon="✈️")

# Replace with your actual Gemini API key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# 2. LOCAL IMAGE BACKGROUND LOGIC

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def set_bg_from_local(bin_file):
    bin_str = get_base64_of_bin_file(bin_file)
    if bin_str:
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                              url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    else:
        st.markdown("<style>.stApp { background: #1e1e2f; }</style>", unsafe_allow_html=True)

set_bg_from_local('background.png') 


# 3. GLOBAL UI STYLING

st.markdown("""
<style>
/* Make all labels and headers Bold and Visible */
.stWidgetLabel p, h1, h2, h3, .stMarkdown p {
    color: white !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.9);
}

/* Bold Tabs */
button[data-baseweb="tab"] p {
    font-size: 18px !important;
    font-weight: 800 !important;
    color: white !important;
}

.main-title {
    text-align: center; font-size: 48px; font-weight: 800; color: white;
    margin-top: 30px; text-shadow: 3px 3px 10px rgba(0,0,0,0.8);
}
.main-subtitle {
    text-align: center; font-size: 20px; color: #dddddd;
    margin-bottom: 30px; text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚉🚗 AI Trip Planner ✈️🚌</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Personalized Travel in Hand</p>", unsafe_allow_html=True)


# 4. DATABASE INITIALIZATION

conn = sqlite3.connect("tripai.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, username TEXT UNIQUE, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS trips (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, city TEXT, days INTEGER, budget INTEGER, interests TEXT, transport TEXT, plan TEXT)")

try:
    c.execute("SELECT transport FROM trips LIMIT 1")
except sqlite3.OperationalError:
    c.execute("ALTER TABLE trips ADD COLUMN transport TEXT")

conn.commit()


# 5. AUTHENTICATION LOGIC

if "user_id" not in st.session_state: st.session_state.user_id = None
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login"

if st.session_state.user_id is None:
    # LOGIN MODE
    if st.session_state.auth_mode == "login":
        st.subheader("🔐 Login")
        login_input = st.text_input("Username or Email", key="log_user")
        password = st.text_input("Password", type="password", key="log_pass")
        if st.button("Login", type="primary", use_container_width=True):
            c.execute("SELECT * FROM users WHERE email=? OR username=?", (login_input.strip(), login_input.strip()))
            user = c.fetchone()
            if user and bcrypt.checkpw(password.strip().encode('utf-8'), user[4].encode('utf-8')):
                st.session_state.user_id = user[0]
                st.rerun()
            else: st.error("Invalid credentials")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Account", use_container_width=True):
                st.session_state.auth_mode = "signup"; st.rerun()
        with col2:
            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.auth_mode = "forgot"; st.rerun()

    # SIGNUP MODE
    elif st.session_state.auth_mode == "signup":
        st.subheader("📝 Register")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        passw = st.text_input("Password", type="password")
        if st.button("Create Account", type="primary", use_container_width=True):
            if name and email and username and passw:
                hashed = bcrypt.hashpw(passw.strip().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                try:
                    c.execute("INSERT INTO users (name,email,username,password) VALUES (?,?,?,?)", (name, email, username, hashed))
                    conn.commit(); st.success("Account created! Please login.")
                    st.session_state.auth_mode = "login"; st.rerun()
                except: st.error("User already exists")
        if st.button("Back to Login", use_container_width=True):
            st.session_state.auth_mode = "login"; st.rerun()

    # FORGOT PASSWORD MODE
    elif st.session_state.auth_mode == "forgot":
        st.subheader("🔑 Reset Password")
        f_email = st.text_input("Registered Email Address")
        f_pass = st.text_input("New Password", type="password")
        if st.button("Update Password", type="primary", use_container_width=True):
            if f_email and f_pass:
                hashed = bcrypt.hashpw(f_pass.strip().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                c.execute("UPDATE users SET password=? WHERE email=?", (hashed, f_email.strip()))
                conn.commit(); st.success("Password updated!"); st.session_state.auth_mode = "login"; st.rerun()
            else: st.warning("Please fill all fields")
        if st.button("Back", use_container_width=True):
            st.session_state.auth_mode = "login"; st.rerun()


# 6. MAIN APP INTERFACE

else:
    with st.sidebar:
        st.title("TripAI Planner")
        if st.button("Logout"): st.session_state.user_id = None; st.rerun()

    tab1, tab2, tab3 = st.tabs(["🏠 PLAN TRIP", "📜 MY TRIPS", "👤 PROFILE"])
    
    with tab1:
        st.markdown("### 📍 **Where to next?**")
        city = st.text_input("Destination City")
        transport = st.selectbox("Means of Transport", ["Flight ✈️", "Train 🚆", "Car 🚗", "Bus 🚌", "Bike 🏍️"])
        days = st.slider("Duration (Days)", 1, 14, 3)
        budget = st.number_input("Budget (₹)", 1000, 500000, 10000)
        interests = st.multiselect("Interests", ["Food", "History", "Nature", "Art", "Adventure", "Nightlife"])
        
        if st.button("Generate AI Itinerary", type="primary"):
            if not city: st.error("Please enter a city.")
            else:
                with st.spinner("Our AI is crafting your trip..."):
                    try:
                        prompt = f"Create a detailed {days}-day itinerary for {city} via {transport}. Budget: ₹{budget}. Interests: {interests}. Focus on {transport} travel tips. Use bold headings and emojis."
                        response = model.generate_content(prompt)
                        plan_text = response.text
                        c.execute("INSERT INTO trips (user_id, city, days, budget, interests, transport, plan) VALUES (?,?,?,?,?,?,?)",
                                  (st.session_state.user_id, city, days, budget, str(interests), transport, plan_text))
                        conn.commit(); st.markdown(plan_text)
                    except Exception as e: st.error(f"AI Error: {e}")

    with tab2:
        st.markdown("### 📜 **Saved Plans**")
        c.execute("SELECT id, city, days, transport, plan FROM trips WHERE user_id=? ORDER BY id DESC", (st.session_state.user_id,))
        for row in c.fetchall():
            with st.expander(f"📍 {row[1]} ({row[3]}) - {row[2]} Days"):
                st.markdown(row[4])
                if st.button("Delete Plan", key=f"del_{row[0]}"):
                    c.execute("DELETE FROM trips WHERE id=?", (row[0],)); conn.commit(); st.rerun()

    with tab3:
        st.markdown("### 👤 **My Profile**")
        c.execute("SELECT name, email, username FROM users WHERE id=?", (st.session_state.user_id,))
        u = c.fetchone()

        if u: st.info(f"**Name:** {u[0]}\n\n**Email:** {u[1]}\n\n**Username:** {u[2]}")
