import streamlit as st
import time
from dialog.create_query import createQueryDialog
from db import get_queries_by_customer

def customer_page():
    @st.dialog("Create Query",dismissible=False,width='medium')
    def createQuery():
        createQueryDialog()
    custom_css="""
<style>
/* Target the main container of Streamlit buttons */
.header-label {
    margin:0 !important;
    padding:0 !important;
}
.stMainBlockContainer{
padding-top: 4rem !important;
padding-left:2rem !important;
padding-right:2rem !important;
}
.st-key-mail-field .error-msg,.st-key-phone-field .error-msg,.st-key-title-field .error-msg,.st-key-desc-field .error-msg{
 font-size:14px !important;
 margin:0 !important;
 color: red;
 margin-left:5px !important;
}
.st-key-mail-field,.st-key-title-field,.st-key-phone-field,.st-key-desc-field{
 gap:4px !important;
}
</style>
"""
    st.markdown(custom_css, unsafe_allow_html=True)
    with st.container(horizontal_alignment="distribute",key='test',horizontal=True):
        st.markdown(f"<h2 class='header-label'>Customer Dashboard — {st.session_state.username}</h2>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
    st.subheader("Your queries")
    df = get_queries_by_customer(st.session_state.user_id)
    
    if df.empty:
        with st.container(horizontal_alignment="distribute",key='filter-container',horizontal=True,vertical_alignment='bottom'):
            status_filter = st.selectbox("Filter by status", ["Open","Closed", "All"],key='filter-status',disabled=True,width=150)
            if st.button("➕ Add New Query"):
                st.session_state.show_add_query_modal=True
        st.info("No queries found.")
        
    else:
        with st.container(horizontal_alignment="distribute",key='filter-container',horizontal=True,vertical_alignment='bottom'):
            status_filter = st.selectbox("Filter by status", ["Open","Closed", "All"],key='filter-status',width=150)
            if status_filter == "All":
                df_filtered = df
            else:
                df_filtered = df[df['status'] == status_filter]
            st.session_state.filtered_data=df_filtered
            if st.session_state.selected_filter!=status_filter:
                st.session_state.selected_filter=status_filter
                st.session_state.close_query_btn=False
            if df_filtered.empty:
                st.info("No queries found for selected filter.")
            addbtn=st.button("➕ Add New Query")
            if addbtn:
                st.session_state.show_add_query_modal=True
        
        column_labels_map = {
            'query_id': 'Id',
            'mail_id': 'Email',
            'mobile_number': 'Mobile Number',
            'query_heading': 'Title',
            'query_description': 'Description',
            'status': 'Status',
            'query_created_date': 'Created Date',
            'query_closed_date': 'Closed Date',
            'user_id': 'User Name'
        }
        config = {}
        for sql_key, display_label in column_labels_map.items():
            config[sql_key] = st.column_config.Column(
                label=display_label
            )
        
        if not df_filtered.empty:
            st.dataframe(df_filtered, 
                        column_config=config,
                        width='stretch',
                        hide_index=True,
                        key='dataframe')
    if st.session_state.show_add_query_modal:
        createQuery()
    # if st.session_state['action_msg']:
    #     if st.session_state['action_msg']['type']=='S':
    #         st.success(st.session_state['action_msg']['msg'])
    #     elif st.session_state['action_msg']['type']=='E':
    #         st.error(st.session_state['action_msg']['msg'])
    #     time.sleep(5)
    #     st.session_state['action_msg']={}

