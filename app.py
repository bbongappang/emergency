import streamlit as st
from src.ui import render_ui

st.set_page_config(
    page_title="Agentic Network Operations 데모",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if __name__ == "__main__":
    render_ui()