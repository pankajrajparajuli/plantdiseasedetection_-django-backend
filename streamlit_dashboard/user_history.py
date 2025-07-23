import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"  # Change if needed

# --- THEME: Wide, dark, green-accented, modern ---
def inject_css():
    st.markdown(
        """
        <style>
        .user-history-table .stDataFrame { min-width: 95vw !important; width: 95vw !important; max-width: 98vw !important; }
        .user-history-filter select, .user-history-filter .stSelectbox>div>div>div>div {
            background: #222 !important; border: none !important; box-shadow: none !important; color: #fff !important;
        }
        .user-history-filter .stSelectbox>div>div>div>div { border: none !important; }
        .user-history-card, .user-history-table, .user-history-modal {
            background: #181818cc !important; border-radius: 14px !important; border: 1.5px solid #2e7d32 !important; box-shadow: 0 4px 32px 0 #000a;
        }
        .user-history-modal-img { max-width: 90vw; max-height: 80vh; border-radius: 10px; border: 2px solid #2e7d32; }
        .user-history-modal-bg { position: fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.85); z-index:9999; display:flex; align-items:center; justify-content:center; }
        .user-history-modal-close { position:absolute; top:2vh; right:3vw; color:#fff; font-size:2.5rem; cursor:pointer; z-index:10000; }
        .user-history-summary { font-size:1.1rem; color:#43a047; margin-bottom:1em; }
        .user-history-pagination { display:flex; gap:0.5em; align-items:center; justify-content:center; margin:1em 0; }
        .user-history-pagination button { background:#2e7d32; color:#fff; border:none; border-radius:6px; padding:0.3em 1em; font-weight:600; }
        .user-history-pagination button:disabled { background:#333; color:#888; }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Helper functions ---
def fetch_users(search=None, start_date=None, end_date=None, page=1, page_size=20):
    params = {"page": page, "page_size": page_size}
    if search:
        params['search'] = search
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    resp = requests.get(f"{API_BASE}/users/", params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_user_history(user_id, page=1, page_size=20, sort_by="-timestamp"):
    params = {"page": page, "page_size": page_size, "ordering": sort_by}
    resp = requests.get(f"{API_BASE}/users/{user_id}/history/", params=params)
    resp.raise_for_status()
    return resp.json()

def delete_prediction(user_id, prediction_id):
    resp = requests.delete(f"{API_BASE}/users/{user_id}/history/{prediction_id}/")
    return resp.status_code == 204

def clear_user_history(user_id):
    resp = requests.delete(f"{API_BASE}/users/{user_id}/history/clear/")
    return resp.status_code == 204

def get_image_from_url(url):
    resp = requests.get(url)
    img = Image.open(BytesIO(resp.content))
    return img

def download_history_csv(history):
    df = pd.DataFrame([
        {
            "Prediction ID": p['id'],
            "Predicted Disease": p['disease'],
            "Confidence (%)": f"{p['confidence']*100:.1f}",
            "Date & Time": p['timestamp'],
        } for p in history
    ])
    return df.to_csv(index=False)

# --- State ---
def init_state():
    for k, v in {
        'selected_user': None,
        'show_image_modal': False,
        'modal_image_url': None,
        'logout_confirm': False,
        'user_page': 1,
        'user_page_size': 20,
        'user_history_page': 1,
        'user_history_page_size': 10,
        'user_history_sort': '-timestamp',
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

def render():
    inject_css()
    init_state()
    st.title("User History Management")
    # --- Logout confirmation dialog ---
    def logout():
        st.session_state['logout_confirm'] = False
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.success("Logged out.")
        st.rerun()
    def logout_button():
        if st.button("Logout", key="logout_btn", help="Logout"):
            st.session_state['logout_confirm'] = True
        if st.session_state.get('logout_confirm', False):
            st.warning("Are you sure you want to logout?", icon="⚠️")
            col1, col2 = st.columns([1,1])
            if col1.button("Yes, Logout", key="yes_logout"):
                logout()
            if col2.button("Cancel", key="cancel_logout"):
                st.session_state['logout_confirm'] = False
    logout_button()

    if st.session_state['selected_user'] is None:
        # --- Level 1: User List ---
        st.subheader("All Users")
        with st.container():
            col1, col2, col3 = st.columns([2,2,2])
            with col1:
                search = st.text_input("Search username/email", key="user_search")
            with col2:
                start_date = st.date_input("Start date", key="user_start_date")
            with col3:
                end_date = st.date_input("End date", key="user_end_date")
        # Pagination
        user_page = st.session_state['user_page']
        user_page_size = st.session_state['user_page_size']
        with st.spinner("Loading users..."):
            users_resp = fetch_users(search, start_date if start_date else None, end_date if end_date else None, page=user_page, page_size=user_page_size)
        users = users_resp.get('results', users_resp) if isinstance(users_resp, dict) else users_resp
        total_users = users_resp.get('count', len(users)) if isinstance(users_resp, dict) else len(users)
        user_rows = []
        for u in users:
            user_rows.append({
                "ID": u['id'],
                "Username": u['username'],
                "Email": u['email'],
                "Total Predictions": u.get('total_predictions', 0),
                "Last Activity": u.get('last_activity', '')
            })
        df = pd.DataFrame(user_rows)
        st.markdown('<div class="user-history-table">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Pagination controls
        total_pages = max(1, (total_users + user_page_size - 1) // user_page_size)
        with st.container():
            st.markdown('<div class="user-history-pagination">', unsafe_allow_html=True)
            prev, next_ = st.columns([1,1])
            if prev.button("Previous", disabled=user_page <= 1, key="user_prev_page"):
                st.session_state['user_page'] -= 1
                st.rerun()
            st.write(f"Page {user_page} of {total_pages}")
            if next_.button("Next", disabled=user_page >= total_pages, key="user_next_page"):
                st.session_state['user_page'] += 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        # Row click: Use selectbox for demo (replace with AgGrid for real click)
        user_ids = [u['ID'] for u in user_rows]
        user_names = [f"{u['Username']} ({u['Email']})" for u in user_rows]
        selected_user = st.selectbox("Select user to view history", options=[None]+user_ids, format_func=lambda x: "Select a user" if x is None else f"{user_rows[user_ids.index(x)]['Username']} ({user_rows[user_ids.index(x)]['Email']})")
        if selected_user:
            st.session_state['selected_user'] = selected_user
            st.session_state['user_history_page'] = 1
            st.rerun()
    else:
        # --- Level 2: User Prediction History ---
        user_id = st.session_state['selected_user']
        st.subheader(f"Prediction History for User ID {user_id}")
        if st.button("Back to User List", key="back_to_user_list"):
            st.session_state['selected_user'] = None
            st.rerun()
        # Sorting
        sort_options = {"Newest": "-timestamp", "Oldest": "timestamp", "Highest Confidence": "-confidence", "Lowest Confidence": "confidence"}
        sort_choice = st.selectbox("Sort by", options=list(sort_options.keys()), key="sort_choice")
        st.session_state['user_history_sort'] = sort_options[sort_choice]
        # Pagination
        page = st.session_state['user_history_page']
        page_size = st.session_state['user_history_page_size']
        with st.spinner("Loading prediction history..."):
            history_resp = fetch_user_history(user_id, page=page, page_size=page_size, sort_by=st.session_state['user_history_sort'])
        history = history_resp.get('results', history_resp) if isinstance(history_resp, dict) else history_resp
        total_preds = history_resp.get('count', len(history)) if isinstance(history_resp, dict) else len(history)
        # Summary
        last_activity = history[0]['timestamp'] if history else "-"
        st.markdown(f'<div class="user-history-summary">Total Predictions: <b>{total_preds}</b> | Last Activity: <b>{last_activity}</b></div>', unsafe_allow_html=True)
        # Download as CSV
        st.download_button("Download as CSV", download_history_csv(history), file_name=f"user_{user_id}_history.csv")
        # Table
        pred_rows = []
        for p in history:
            pred_rows.append({
                "Prediction ID": p['id'],
                "Plant Image": p['image_url'],
                "Predicted Disease": p['disease'],
                "Confidence (%)": f"{p['confidence']*100:.1f}",
                "Date & Time": p['timestamp']
            })
        df = pd.DataFrame(pred_rows)
        st.markdown('<div class="user-history-table">', unsafe_allow_html=True)
        for idx, row in df.iterrows():
            cols = st.columns([2,3,3,2,3,2])
            cols[0].write(row['Prediction ID'])
            if row['Plant Image']:
                if cols[1].button("View", key=f"view_img_{row['Prediction ID']}"):
                    st.session_state['show_image_modal'] = True
                    st.session_state['modal_image_url'] = row['Plant Image']
                img = get_image_from_url(row['Plant Image'])
                cols[1].image(img, width=60)
            else:
                cols[1].write("-")
            cols[2].write(row['Predicted Disease'])
            cols[3].write(row['Confidence (%)'])
            cols[4].write(row['Date & Time'])
            if cols[5].button("Delete", key=f"del_pred_{row['Prediction ID']}"):
                if st.session_state.get(f'confirm_del_{row["Prediction ID"]}', False) or st.confirm(f"Delete prediction {row['Prediction ID']}?", key=f"confirm_del_{row['Prediction ID']}"):
                    if delete_prediction(user_id, row['Prediction ID']):
                        st.success("Prediction deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete prediction.")
        st.markdown('</div>', unsafe_allow_html=True)
        # Pagination controls
        total_pages = max(1, (total_preds + page_size - 1) // page_size)
        with st.container():
            st.markdown('<div class="user-history-pagination">', unsafe_allow_html=True)
            prev, next_ = st.columns([1,1])
            if prev.button("Previous", disabled=page <= 1, key="history_prev_page"):
                st.session_state['user_history_page'] -= 1
                st.rerun()
            st.write(f"Page {page} of {total_pages}")
            if next_.button("Next", disabled=page >= total_pages, key="history_next_page"):
                st.session_state['user_history_page'] += 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        # Clear all history
        if st.button("Clear All History for this User", key="clear_all_history"):
            if st.confirm("Are you sure you want to clear all history for this user?", key="confirm_clear_all"):
                if clear_user_history(user_id):
                    st.success("All history cleared.")
                    st.rerun()
                else:
                    st.error("Failed to clear history.")
        # Modal for full-size image
        if st.session_state.get('show_image_modal', False) and st.session_state.get('modal_image_url'):
            st.markdown(f'''<div class="user-history-modal-bg" onclick="this.style.display='none';">
                <span class="user-history-modal-close" onclick="this.parentElement.style.display='none'; event.stopPropagation();">&times;</span>
                <img src="{st.session_state['modal_image_url']}" class="user-history-modal-img" />
            </div>''', unsafe_allow_html=True)
            if st.button("Close Image", key="close_img_modal"):
                st.session_state['show_image_modal'] = False
                st.session_state['modal_image_url'] = None
                st.rerun() 