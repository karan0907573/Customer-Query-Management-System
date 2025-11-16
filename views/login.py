import streamlit as st
from db import get_user_by_username
from auth import verify_password, register_user


def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["client", "support"])
        submitted = st.form_submit_button("Login")
    st.markdown("---")
    if submitted:
        user = get_user_by_username(username)
        if not user:
            st.error("No user found.")
            return
        if user['role'] != role:
            st.error("Role mismatch for this user.")
            return
        if verify_password(password, user['hashed_password']):
            st.success("Logged in.")
            st.session_state.logged_in = True
            st.session_state.user_id = user['username']
            st.session_state.username = user['username']
            st.session_state.role = user['role']
            st.rerun()
        else:
            st.error("Invalid credentials.")

    st.write("----")
    with st.expander("Create a test user (admin/dev only)"):
        st.write("Use this to create sample users quickly.")
        with st.form("create_user_form"):
            new_un = st.text_input("New username")
            new_pw = st.text_input("New password", type="password")
            new_role = st.selectbox("Role", ["client", "support"])
            create_sub = st.form_submit_button("Create user")
        if create_sub:
            try:
                register_user(new_un, new_pw, new_role)
                st.success("User created. Now login.")
            except Exception as e:
                st.error(f"Error: {e}")
