import sys
import os
import django

# Get the project root (one level above this file)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the settings module (change 'plantguard' if your folder name is different)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantguard.settings')

# Setup Django
django.setup()

# safely import other Django-related code
import utils

import streamlit as st
from streamlit_option_menu import option_menu
import users
import predictions
import model_manager
import user_history

# --- THEME: Green Navbar, Black Main Background, Small Login Box ---
st.markdown("""
<style>
:root {
  --main-green: #2e7d32;
  --main-green-dark: #205723;
  --accent-green: #43a047;
  --white: #fff;
  --main-black: #111;
}
section[data-testid="stSidebar"] {
  background: var(--main-green) !important;
  color: var(--white) !important;
}
section[data-testid="stSidebar"] .css-1v3fvcr,
section[data-testid="stSidebar"] .css-1lcbmhc {
  background: transparent !important;
}
section[data-testid="stSidebar"] .css-1v3fvcr * {
  color: var(--white) !important;
}
section[data-testid="stSidebar"] .stButton>button {
  background: var(--accent-green) !important;
  color: var(--white) !important;
  border-radius: 8px !important;
  border: none !important;
}
section[data-testid="stSidebar"] .stButton>button:hover {
  background: var(--main-green-dark) !important;
}
.st-emotion-cache-10trblm, .st-emotion-cache-1v3fvcr {
  color: var(--white) !important;
}
.st-emotion-cache-1v3fvcr .nav-link-selected {
  background: var(--accent-green) !important;
  color: var(--white) !important;
  border-radius: 8px;
}
.stApp {
  background: var(--main-black) !important;
}
/* Make all text white by default in main area */
.stApp, .stApp * {
  color: var(--white) !important;
}
/* Remove green surface from dashboard components, make them transparent/dark */
.stMetric, .stForm, .stDataFrame, .stTable, .stExpander, .stAlert {
  background: transparent !important;
  border-radius: 12px !important;
  border: none !important;
  color: var(--white) !important;
  box-shadow: none !important;
}
.stExpanderHeader {
  color: var(--main-green) !important;
}
.stTextInput>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div>div {
  border: 1.5px solid var(--main-green) !important;
  border-radius: 6px !important;
  background: #222 !important;
  color: var(--white) !important;
}
/* Small, centered login box, modern look */
.login-container {
  max-width: 340px;
  margin: 8vh auto 0 auto;
  background: #181818cc;
  border-radius: 18px;
  box-shadow: 0 4px 32px 0 #000a;
  padding: 2.5em 2em 2em 2em;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1.5px solid var(--main-green);
}
.login-header {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent-green);
  margin-bottom: 1.2em;
  letter-spacing: 1px;
  text-align: center;
}
.login-container h1, .login-container label, .login-container input {
  color: var(--white) !important;
}
.login-container .stTextInput>div>input {
  background: #222 !important;
  border: 1.5px solid var(--main-green) !important;
  color: var(--white) !important;
}
.login-container .stButton>button {
  background: var(--main-green) !important;
  color: var(--white) !important;
  border-radius: 8px !important;
  border: none !important;
  font-weight: 600;
  margin-top: 1em;
}
.login-container .stButton>button:hover {
  background: var(--accent-green) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session State for Auth ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login():
    # Only render login-container when login form is present and not empty
    login_html = '''<div class="login-container">
    <div class="login-header">Plant Guard Admin Login</div>
    '''
    st.markdown(login_html, unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if utils.is_superuser(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials or not a superuser.")
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.success("Logged out.")
    st.rerun()

if not st.session_state['logged_in']:
    login()
    st.stop()

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/admin-settings-male.png", width=80)
    st.markdown(f"**Logged in as:** <span style='color:#fff'>{st.session_state['username']}</span>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Users", "User History", "Predictions", "History", "Model Management", "Settings", "Logout"],
        icons=["speedometer", "people", "clock-history", "activity", "clock-history", "cloud-upload", "gear", "box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#2e7d32", "border-radius": "10px"},
            "icon": {"color": "#fff", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "color": "#fff", "--hover-color": "#43a047"},
            "nav-link-selected": {"background-color": "#43a047", "color": "#fff", "font-weight": "bold"},
        }
    )

# --- Main Content ---
if selected == "Dashboard":
    st.title("\U0001F4CA Dashboard")
    metrics = utils.get_user_metrics()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", metrics['total_users'])
    col2.metric("Total Predictions", metrics['total_predictions'])
    col3.metric("Most Predicted Disease", metrics['most_predicted'])

    import plotly.express as px

    st.subheader("User Growth Over Time")
    df_users = utils.get_user_growth()
    if not df_users.empty:
        fig = px.line(df_users, x='date', y='count', title='User Growth', color_discrete_sequence=["#2e7d32"])
        fig.update_layout(plot_bgcolor="#111", paper_bgcolor="#111", font_color="#43a047")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No user data available.")

    st.subheader("Predictions by Disease")
    df_pred = utils.get_predictions_by_disease()
    if not df_pred.empty:
        fig2 = px.bar(df_pred, x='disease', y='count', title='Predictions by Disease', color_discrete_sequence=["#2e7d32"])
        fig2.update_layout(plot_bgcolor="#111", paper_bgcolor="#111", font_color="#43a047")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No prediction data available.")

    st.subheader("Predictions Per Day")
    df_per_day = utils.get_predictions_per_day()
    if not df_per_day.empty:
        fig3 = px.area(df_per_day, x='date', y='count', title='Predictions Per Day', color_discrete_sequence=["#2e7d32"])
        fig3.update_layout(plot_bgcolor="#111", paper_bgcolor="#111", font_color="#43a047")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No daily prediction data available.")

elif selected == "Users":
    users.render()

elif selected == "User History":
    user_history.render()

elif selected == "Predictions":
    predictions.render_predictions()

elif selected == "History":
    predictions.render_history()

elif selected == "Model Management":
    model_manager.render()

elif selected == "Settings":
    st.title("\u2699\ufe0f Settings")
    st.info("Settings page coming soon.")

elif selected == "Logout":
    if "confirm_logout" not in st.session_state:
        st.session_state["confirm_logout"] = False

    else:
        # Confirmation UI
        st.warning("Are you sure you want to log out?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Logout"):
                logout()  # Call your logout function
                st.session_state["confirm_logout"] = False
                st.rerun()
