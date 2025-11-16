import streamlit as st
import time
from db import close_query

def closeQueryDialog(data):
    if(not(data)):
         data={'query_id':None,"query_description":None,"query_heading":None}
    with st.form("update_ticket_form"):
            qid =data['query_id']
            st.markdown(f"<h4>Query id: {qid}</h4>",unsafe_allow_html=True)
            status = st.selectbox("Status", ["Open","Closed"],disabled=True)
            st.text_input('Title',disabled=True,value=data['query_heading'])
            st.text_area('Description',disabled=True,value=data['query_description'])
            with st.container(horizontal=True,horizontal_alignment='right'):
                cancel = st.form_submit_button("Cancel")
                upd = st.form_submit_button("Proceed")
            if upd:
                try:
                    print(status)
                    if status == 'Open':
                        close_query(qid)
                        st.success("Query closed.")
                        time.sleep(3)
                        st.session_state.close_ticket_dialog=False
                        st.rerun()
                except Exception as e:
                    print(e)
                    st.error(f"Failed: {e}")
                    time.sleep(3)
                    st.session_state.close_ticket_dialog=False
                    st.rerun()
            if cancel:
                st.session_state.close_ticket_dialog=False
                st.rerun()