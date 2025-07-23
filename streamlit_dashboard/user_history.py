import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import jwt_auth

API_BASE = "http://127.0.0.1:8000/api/account"  # Change if needed

# --- Minimal CSS ---
def inject_css():
    st.markdown(
        """
        <style>
        .user-history-table .stDataFrame { min-width: 95vw !important; width: 95vw !important; max-width: 98vw !important; }
        .user-history-card, .user-history-table {
            background: #1e1e1e !important; border-radius: 8px !important; border: 1px solid #444 !important; 
        }
        .user-history-summary { font-size:1rem; color:#ccc; margin-bottom:1em; }
        </style>
        """,
        unsafe_allow_html=True
    )


# --- Helper functions ---
def fetch_users(search=None, start_date=None, end_date=None, page=1, page_size=10):
    params = {"page": page, "page_size": page_size}
    if search:
        params['search'] = search
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    return jwt_auth.authorized_get(f"{API_BASE}/users/", params=params)


def fetch_user_history(user_id, page=1, page_size=10, sort_by="-timestamp"):
    params = {"page": page, "page_size": page_size, "ordering": sort_by}
    return jwt_auth.authorized_get(f"{API_BASE}/users/{user_id}/history/", params=params)


def delete_prediction(user_id, prediction_id):
    resp = jwt_auth.authorized_delete(f"{API_BASE}/users/{user_id}/history/{prediction_id}/delete/")
    return resp and resp.status_code == 204


def clear_user_history(user_id):
    resp = jwt_auth.authorized_delete(f"{API_BASE}/users/{user_id}/history/clear/")
    return resp and resp.status_code == 204


def download_history_csv(history):
    df = pd.DataFrame([
        {
            "Prediction ID": p['id'],
            "Predicted Disease": p['disease'],
            "Confidence (%)": f"{p['confidence'] * 100:.1f}",
            "Date & Time": p['timestamp'],
        } for p in history
    ])
    return df.to_csv(index=False)


# --- State ---
def init_state():
    for k, v in {
        'selected_user': None,
        'user_page': 1,
        'user_page_size': 10,
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

    # ---------------- USERS LIST PAGE ----------------
    if st.session_state['selected_user'] is None:
        st.subheader("All Users")
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            search = st.text_input("Search username/email", key="user_search")
        with col2:
            start_date = st.date_input("Start date", key="user_start_date")
        with col3:
            end_date = st.date_input("End date", key="user_end_date")

        user_page = st.session_state['user_page']
        user_page_size = st.session_state['user_page_size']
        with st.spinner("Loading users..."):
            users_resp = fetch_users(search, start_date if start_date else None, end_date if end_date else None,
                                     page=user_page, page_size=user_page_size)

        users = users_resp  # Assume list
        total_users = len(users)

        user_rows = [{"ID": u['id'], "Username": u['username'], "Email": u['email'],
                      "Total Predictions": u.get('total_predictions', 0),
                      "Last Activity": u.get('last_activity', '')} for u in users]
        df = pd.DataFrame(user_rows)
        st.dataframe(df, use_container_width=True)

        total_pages = max(1, (total_users + user_page_size - 1) // user_page_size)
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("Previous", disabled=user_page <= 1):
                st.session_state['user_page'] -= 1
                st.rerun()
        with col_page:
            st.write(f"Page {user_page} of {total_pages}")
        with col_next:
            if st.button("Next", disabled=user_page >= total_pages):
                st.session_state['user_page'] += 1
                st.rerun()

        selected_user = st.selectbox("Select user to view history",
                                     options=[None] + [u['ID'] for u in user_rows],
                                     format_func=lambda x: "Select a user" if x is None else f"User ID {x}")
        if selected_user:
            st.session_state['selected_user'] = selected_user
            st.session_state['user_history_page'] = 1  # reset history pagination
            st.rerun()

    # ---------------- USER HISTORY PAGE ----------------
    else:
        user_id = st.session_state['selected_user']
        st.subheader(f"Prediction History for User ID {user_id}")
        if st.button("Back to User List"):
            st.session_state['selected_user'] = None
            st.rerun()

        sort_choice = st.selectbox("Sort by", options=["Newest", "Oldest", "Highest Confidence", "Lowest Confidence"])
        sort_mapping = {"Newest": "-timestamp", "Oldest": "timestamp",
                        "Highest Confidence": "-confidence", "Lowest Confidence": "confidence"}
        st.session_state['user_history_sort'] = sort_mapping[sort_choice]

        page = st.session_state['user_history_page']
        page_size = st.session_state['user_history_page_size']
        with st.spinner("Loading prediction history..."):
            history_resp = fetch_user_history(user_id, page=page, page_size=page_size,
                                              sort_by=st.session_state['user_history_sort'])

        if hasattr(history_resp, 'status_code'):
            if history_resp.status_code != 200:
                st.error(f"Failed to fetch history: {history_resp.status_code}")
                return
            history_data = history_resp.json()
            history = history_data.get('results', history_data) if isinstance(history_data, dict) else history_data
        else:
            history = history_resp
            history_data = {"count": len(history)}

        total_preds = history_data.get('count', len(history)) if isinstance(history_data, dict) else len(history)
        if total_preds == 0:
            st.info("No predictions to delete.")
            if st.button("Back to User List"):
                st.session_state['selected_user'] = None
                st.rerun()
            return

        st.markdown(
            f'<div class="user-history-summary">Total Predictions: <b>{total_preds}</b></div>',
            unsafe_allow_html=True)

        st.download_button("Download as CSV", download_history_csv(history), file_name=f"user_{user_id}_history.csv")

        # Table with one-click delete
        for p in history:
            cols = st.columns([2, 3, 2, 3, 2])
            cols[0].write(p['id'])
            cols[1].write(p['disease'])
            cols[2].write(f"{p['confidence'] * 100:.1f}")
            cols[3].write(p['timestamp'])
            if cols[4].button(f"Delete {p['id']}", key=f"del_{p['id']}"):
                if delete_prediction(user_id, p['id']):
                    st.success(f"Deleted prediction {p['id']}")
                    st.rerun()
                else:
                    st.error("Failed to delete prediction.")

        # Pagination for history
        total_pages = max(1, (total_preds + page_size - 1) // page_size)
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("Previous", disabled=page <= 1):
                st.session_state['user_history_page'] -= 1
                st.rerun()
        with col_page:
            st.write(f"Page {page} of {total_pages}")
        with col_next:
            if st.button("Next", disabled=page >= total_pages):
                st.session_state['user_history_page'] += 1
                st.rerun()

        # Clear all history
        if st.checkbox("I confirm I want to delete ALL history for this user"):
            if st.button("Clear All History for this User"):
                if clear_user_history(user_id):
                    st.success("All history cleared.")
                    st.rerun()
                else:
                    st.error("Failed to clear history.")


if __name__ == "__main__":
    render()
