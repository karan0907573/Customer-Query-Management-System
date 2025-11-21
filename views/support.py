import streamlit as st
import pandas as pd
from db import get_queries
from dialog.close_query import closeQueryDialog


def callback():
    selected_data=st.session_state.dataframe
    if selected_data.selection['rows']:
        selected_row=selected_data.selection['rows'][0]
        df=st.session_state.filtered_data
        first_row = df.iloc[selected_row]
        if first_row['status']=='Open':
            st.session_state.close_query_btn=True
            st.session_state.query_data=first_row.to_dict()
        else:
            st.session_state.close_query_btn=False
    else:
        st.session_state.close_query_btn=False
    print('**********')

def support_page():
    
    @st.dialog("Close Query",dismissible=False,width='medium')
    def closeQuery(data):
        closeQueryDialog(data)
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
</style>
"""
    st.markdown(custom_css, unsafe_allow_html=True)
    with st.container(horizontal_alignment="distribute",key='test',horizontal=True):
        st.markdown(f"<h2 class='header-label'>Support Dashboard — {st.session_state.username}</h2>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
    df = get_queries()
    
    st.subheader("Client queries")
    
    if df.empty:
        with st.container(horizontal_alignment="distribute",key='filter-container',horizontal=True,vertical_alignment='bottom'):
            status_filter = st.selectbox("Filter by status", ["Open","Closed", "All"],key='filter-status',disabled=True,width=150)
            close_btn=st.button('Close',disabled=True)
        st.info("No queries found.")
        return
    
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
        
        # Only show Close button for Open or All status filters
        if status_filter != "Closed":
            close_btn=st.button('Close',disabled=not(st.session_state.close_query_btn))
            if close_btn:
                st.session_state.close_ticket_dialog=True

    if st.session_state.close_ticket_dialog:
        st.session_state.close_query_btn=False
        closeQuery(st.session_state.query_data)
    elif not df_filtered.empty:
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
        
        # Only enable selection mode for Open or All status filters
        if status_filter == "Closed":
            st.dataframe(df_filtered, 
                        column_config=config,
                        width='stretch',
                        hide_index=True,
                        key='dataframe')
        else:
            st.dataframe(df_filtered, 
                        column_config=config,
                        width='stretch',
                        on_select=callback,
                        hide_index=True,
                        selection_mode='single-row',
                        key='dataframe')
            

