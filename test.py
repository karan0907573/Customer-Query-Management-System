import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((12, 5)), columns=["a", "b", "c", "d", "e"]
)

event = st.dataframe(
    df,
    key="data",
    on_select="rerun",
    selection_mode=["single-row", "multi-column", "multi-cell"],
)
btn=st.button("clear")
if btn:
    event.selection['rows']
    print(event.selection['rows'])
event.selection