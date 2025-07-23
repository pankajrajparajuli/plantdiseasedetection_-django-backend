import streamlit as st
import pandas as pd
from django.contrib.auth.models import User
import utils

def render():
    st.title("\U0001F465 User Management")
    st.markdown("Manage users: add, edit, delete, and export.")

    # --- Custom CSS for wider table, dropdowns, and to hide checkmark ---
    st.markdown(
        """
        <style>
        .stTextInput > div > input,
        .stTextArea > div > textarea,
        .stSelectbox > div > div > div > div {
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            color: inherit !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Search and Filter ---
    search = st.text_input("Search by username or email")
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.container():
            st.markdown('<div class="user-filter">', unsafe_allow_html=True)
            is_staff = st.selectbox("Staff status", options=["All", "Staff", "Non-staff"])
            st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown('<div class="user-filter">', unsafe_allow_html=True)
            is_superuser = st.selectbox("Superuser status", options=["All", "Superuser", "Regular"])
            st.markdown('</div>', unsafe_allow_html=True)

    staff_val = None if is_staff == "All" else (is_staff == "Staff")
    superuser_val = None if is_superuser == "All" else (is_superuser == "Superuser")

    users_qs = utils.get_users(search=search, is_staff=staff_val, is_superuser=superuser_val)
    users_list = list(users_qs.values('id', 'username', 'email', 'is_staff', 'is_superuser', 'date_joined'))

    # --- Wider table container ---
    st.markdown('<div class="user-table-container">', unsafe_allow_html=True)
    df = pd.DataFrame(users_list)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Export as CSV ---
    st.download_button("Export as CSV", df.to_csv(index=False), "users.csv")

    # --- Add/Edit User ---
    with st.expander("\u2795 Add New User"):
        with st.form("add_user_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            is_staff = st.checkbox("Is Staff")
            is_superuser = st.checkbox("Is Superuser")
            submit = st.form_submit_button("Add User")
            if submit:
                if User.objects.filter(username=username).exists():
                    st.error("Username already exists.")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.is_staff = is_staff
                    user.is_superuser = is_superuser
                    user.save()
                    st.success("User added successfully.")
                    st.rerun()

    # --- Edit/Delete User ---
    st.markdown("### Edit or Delete Users")
    for idx, row in df.iterrows():
        with st.expander(f"Edit/Delete: {row['username']}"):
            with st.form(f"edit_user_{row['id']}"):
                new_email = st.text_input("Email", value=row['email'])
                new_is_staff = st.checkbox("Is Staff", value=row['is_staff'])
                new_is_superuser = st.checkbox("Is Superuser", value=row['is_superuser'])
                new_password = st.text_input("New Password (leave blank to keep unchanged)", type="password")
                update = st.form_submit_button("Update")
                delete = st.form_submit_button("Delete", type="primary")
                if update:
                    user = User.objects.get(id=row['id'])
                    user.email = new_email
                    user.is_staff = new_is_staff
                    user.is_superuser = new_is_superuser
                    if new_password:
                        user.set_password(new_password)
                    user.save()
                    st.success("User updated.")
                    st.rerun()
                if delete:
                    if st.warning("Are you sure you want to delete this user? This action cannot be undone.", icon="\u26a0\ufe0f"):
                        User.objects.get(id=row['id']).delete()
                        st.success("User deleted.")
                        st.rerun()