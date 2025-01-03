import streamlit as st
import sqlite3
import os
import pandas as pd
import utils
import streamlit as st
import sqlalchemy

conn = utils.get_database_connection()

def dashboard():
    st.title("Dashboard")
    st.write("Welcome to the Dashboard! This is the main page.")

import streamlit as st
import sqlite3

# Database connection
def get_database_connection():
    return sqlite3.connect("persistent_data.db")  # Replace with your DB path if needed

# Main function for Neighborhoods Page
def neighborhoods():
    st.title("Neighborhoods")

    # Connect to the database
    conn = get_database_connection()
    cursor = conn.cursor()

    # Fetch unique neighborhood codes
    cursor.execute('''
                   SELECT DISTINCT "Neighborhood Code" 
                   FROM neighborhood_multipliers;
                   ''')
    neighborhoods = [row[0] for row in cursor.fetchall()]

    # Fetch current data from neighborhood_multipliers
    cursor.execute('''SELECT "Neighborhood Code", is_set, percentage FROM neighborhood_multipliers;''')
    multipliers = {row[0]: {'is_set': bool(row[1]), 'percentage': row[2]} for row in cursor.fetchall()}

    # Create a form for user inputs
    with st.form("neighborhood_form"):
        for neighborhood in neighborhoods:
            col1, col2, col3 = st.columns([2, 1, 2])

            # Display neighborhood code
            col1.write(neighborhood)

            # Checkbox for is_set
            is_set = col2.checkbox("Set", value=multipliers.get(neighborhood, {}).get('is_set', False), key=f"{neighborhood}_set")

            # Input for percentage
            percentage = col3.number_input(
                "Percentage",
                min_value=0.0,
                max_value=100.0,
                value=multipliers.get(neighborhood, {}).get('percentage', 0.0),
                step=0.001,
                key=f"{neighborhood}_percentage"
            )

            # Store the updated values in session state
            st.session_state[neighborhood] = {'is_set': is_set, 'percentage': percentage}

        # Submit button
        submit = st.form_submit_button("Save Changes")

        if submit:
            # Update database with user inputs
            for neighborhood, values in st.session_state.items():
                is_set = int(values['is_set'])
                percentage = values['percentage']

                cursor.execute('''
                    INSERT INTO neighborhood_multipliers ("Neighborhood Code", is_set, percentage)
                    VALUES (?, ?, ?)
                    ON CONFLICT("Neighborhood Code")
                    DO UPDATE SET is_set = ?, percentage = ?;
                ''', (neighborhood, is_set, percentage, is_set, percentage))

            conn.commit()
            st.success("Neighborhood multipliers updated successfully!")

    # Close the database connection
    conn.close()

def reports():
    st.title("Reports")
    st.write("Access all your reports here.")

# Map custom names to page functions
pages = {
    "🏠 Dashboard": dashboard,
    "📊 Neighborhoods": neighborhoods,
    "📄 Reports": reports,
}

# Sidebar navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("", pages.keys())

# Display the selected page
pages[selected_page]()
