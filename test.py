import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter


st.set_page_config(page_title="Mapping Demo", page_icon="🌍")
# Define your data
# Assuming style.css is properly configured for Streamlit
with open('./style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
col1, col2 = st.columns(2)
col1.metric("Yes", "2")
col2.metric("No", "1")
# col3.metric("dfd", "1")

# Display the table

