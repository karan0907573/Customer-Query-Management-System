import streamlit as st
import time
import streamlit.components.v1 as components
import re
from db import create_query

def validateEmail(val):
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", val):
        return True, ""
    elif(not(len(val))):
        return False,"Please fill Email"
    else:
        return False, "Invalid email format."
    
def validateMobileNumber(val):
     if val.isdigit() and len(val) == 10:
         return True, ""
     elif(not(len(val))):
         return False,"Please fill Phone Number"
     else:
         return False,"Not a valid Phone Number"
def validateTitle(val):
    if(not(len(val))):
         return False,"Please fill Title"
    else:
         return True,""
def validateDesc(val):
     if(not(len(val))):
         return False,"Please fill Description"
     else:
         return True,""
def createQueryDialog():
    print('session')
    with st.form("Create a Query:"):
            valid_number=False
            valid_email=False
            valid_title=False
            valid_desc=False
            msg=None
            with st.container(key='title-field'):
                title=(st.text_input('Title',max_chars=250)).strip()
                if st.session_state.create_query_submitted:
                    valid_title,msg=validateTitle(title)
                    not(valid_title) and st.markdown(f"""<p class="error-msg">{msg}</p>""",unsafe_allow_html=True)
            with st.container(key='desc-field'):
                description=(st.text_area('Description',max_chars=400)).strip()
                if st.session_state.create_query_submitted:
                    valid_desc,msg=validateDesc(description)
                    not(valid_desc) and st.markdown(f"""<p class="error-msg">{msg}</p>""",unsafe_allow_html=True)
            with st.container(key='mail-field'):
                email=(st.text_input('Mail',max_chars=100)).strip()
                if st.session_state.create_query_submitted:
                    valid_email,msg=validateEmail(email)
                    not(valid_email) and st.markdown(f"""<p class="error-msg">{msg}</p>""",unsafe_allow_html=True)
            with st.container(key='phone-field'):
                phonenumber=(st.text_input(
                    'Phone No',
                    key='phone_field',
                    max_chars=10
                    )).strip()
                if st.session_state.create_query_submitted:
                    valid_number,msg=validateMobileNumber(phonenumber.strip())
                    not(valid_number) and st.markdown(f"""<p class="error-msg">{msg}</p>""",unsafe_allow_html=True)
            if st.session_state.create_query_submitted:
                # res_msg={}

                try:
                    if(valid_email and valid_number and valid_desc and valid_title):
                        create_query(email,phonenumber,title,description,st.session_state.user_id)
                        # res_msg["type"] = "S"
                        # res_msg["msg"] = "Query Raised Successfully"
                        # st.session_state.action_msg=res_msg
                        st.success("Query Raised Successfully")
                        st.session_state.create_query_submitted=False
                        st.session_state.show_add_query_modal=False
                        time.sleep(4)
                        st.rerun()
                except Exception as e:
                    # res_msg["type"] = "E"
                    # res_msg["msg"] = (f"Failed: {e}")
                    # st.session_state.action_msg=res_msg
                    st.error((f"Failed: {e}"))
                    st.session_state.create_query_submitted=False
                    st.session_state.show_add_query_modal=False
                    time.sleep(4)
                    st.rerun()
            with st.container(horizontal=True,horizontal_alignment='right'):
                cancel = st.form_submit_button("Cancel")
                upd = st.form_submit_button("Proceed")
                if upd:
                    if(not(st.session_state.create_query_submitted)):
                        st.session_state.create_query_submitted=True
                        st.rerun()
                    
                if cancel:
                    st.session_state.show_add_query_modal=False
                    st.session_state.create_query_submitted=False
                    st.rerun()