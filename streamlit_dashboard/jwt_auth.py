import streamlit as st
import requests
import time

API_BASE = "http://127.0.0.1:8000/api/account"
TOKEN_URL = "http://127.0.0.1:8000/api/account/login/"
REFRESH_URL = "http://127.0.0.1:8000/api/account/refresh/"


def login_and_store_tokens(username, password):
    resp = requests.post(TOKEN_URL, data={"username": username, "password": password})
    if resp.status_code == 200:
        tokens = resp.json()
        st.session_state['access_token'] = tokens['access']
        st.session_state['refresh_token'] = tokens['refresh']
        st.session_state['token_time'] = time.time()
        return True
    else:
        st.error("Login failed: " + resp.text)
        return False


def get_access_token():
    access = st.session_state.get('access_token')
    refresh = st.session_state.get('refresh_token')
    token_time = st.session_state.get('token_time', 0)
    if not access or not refresh or (time.time() - token_time > 240):
        if not refresh:
            return None
        resp = requests.post(REFRESH_URL, data={"refresh": refresh})
        if resp.status_code == 200:
            access = resp.json()['access']
            st.session_state['access_token'] = access
            st.session_state['token_time'] = time.time()
        else:
            st.error("Session expired. Please log in again.")
            st.session_state['access_token'] = None
            st.session_state['refresh_token'] = None
            return None
    return st.session_state['access_token']


def authorized_get(url, params=None):
    token = get_access_token()
    if not token:
        st.error("Not authenticated.")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 401:
        st.session_state['access_token'] = None
        token = get_access_token()
        if not token:
            st.error("Session expired. Please log in again.")
            return None
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error(f"API error: {resp.status_code} {resp.text}")
        return None


def authorized_post(url, data=None, json=None):
    token = get_access_token()
    if not token:
        st.error("Not authenticated.")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(url, headers=headers, data=data, json=json)
    return resp


def authorized_delete(url):
    token = get_access_token()
    if not token:
        st.error("Not authenticated.")
        return None
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers)
    return resp
