import streamlit as st
from streamlit_option_menu import option_menu
import utils
import users
import predictions
import model_manager

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# --- Session State for Auth ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login():
    st.title("Admin Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if utils.is_superuser(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials or not a superuser.")

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.success("Logged out.")
    st.experimental_rerun()

if not st.session_state['logged_in']:
    login()
    st.stop()

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/000000/admin-settings-male.png", width=80)
    st.markdown(f"**Logged in as:** {st.session_state['username']}")
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "Users", "Predictions", "History", "Model Management", "Settings", "Logout"],
        icons=["speedometer", "people", "activity", "clock-history", "cloud-upload", "gear", "box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8fafc"},
            "icon": {"color": "#0d6efd", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#e2e8f0"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
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
        fig = px.line(df_users, x='date', y='count', title='User Growth')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No user data available.")

    st.subheader("Predictions by Disease")
    df_pred = utils.get_predictions_by_disease()
    if not df_pred.empty:
        fig2 = px.bar(df_pred, x='disease', y='count', title='Predictions by Disease')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No prediction data available.")

    st.subheader("Predictions Per Day")
    df_per_day = utils.get_predictions_per_day()
    if not df_per_day.empty:
        fig3 = px.area(df_per_day, x='date', y='count', title='Predictions Per Day')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No daily prediction data available.")

elif selected == "Users":
    users.render()

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
    logout() 