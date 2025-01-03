from sqlalchemy import create_engine
import streamlit as st

# Define a function to connect to the database
@st.cache_resource
def get_database_connection():
    db_path = "/workspaces/skagit-regression/persistent_data.db"
    """Connect to the SQLite database and return the engine object."""
    engine = create_engine(f"sqlite:///{db_path}")
    return engine



