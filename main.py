import streamlit as st
import pandas as pd
from views.login import login_page
from views.customer import customer_page
from views.support import support_page

st.set_page_config(page_title="Customer Query Management", layout="wide")

# ---------- session helpers ----------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'show_add_query_modal' not in st.session_state:
    st.session_state.show_add_query_modal = False
if 'close_ticket_dialog' not in st.session_state:
    st.session_state.close_ticket_dialog = False
if 'close_query_btn' not in st.session_state:
    st.session_state.close_query_btn=False
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data=pd.DataFrame()
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter=None
if 'query_data' not in st.session_state:
    st.session_state.query_data=None
if 'create_query_submitted' not in st.session_state:
    st.session_state.create_query_submitted=False
# if 'action_msg' not in st.session_state:
#     st.session_state.action_msg=''

# ---------- main ----------
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.role == 'client':
            customer_page()
        elif st.session_state.role == 'support':
            support_page()
        else:
            st.error("Unknown role. Please logout and login again.")

if __name__ == "__main__":
    main()
