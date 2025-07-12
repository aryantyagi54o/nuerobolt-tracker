import streamlit as st
import sqlite3
from datetime import date

# Database setup
conn = sqlite3.connect("aiml_tracker.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        question_name TEXT,
        topic TEXT,
        difficulty TEXT,
        status TEXT
    )
''')
conn.commit()

# Functions
def add_entry(username, date, question_name, topic, difficulty, status):
    cursor.execute("INSERT INTO progress (username, date, question_name, topic, difficulty, status) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, date, question_name, topic, difficulty, status))
    conn.commit()

def fetch_entries(username):
    if username.lower() == "aryan":
        cursor.execute("SELECT * FROM progress ORDER BY date DESC")
    else:
        cursor.execute("SELECT * FROM progress WHERE username = ? ORDER BY date DESC", (username,))
    return cursor.fetchall()

# Streamlit UI
st.title("NeuroBolt AIML Progress Tracker")

# --- Login Page ---
if 'username' not in st.session_state:
    st.subheader("🔐 Login")
    username_input = st.text_input("Enter your username")
    if st.button("Login"):
        if username_input:
            st.session_state.username = username_input
            st.success(f"Welcome {username_input}!")
            st.experimental_rerun()
        else:
            st.warning("Please enter a username to continue.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    username = st.session_state.username

    menu = st.sidebar.selectbox("Menu", ["➕ Add Entry", "📋 View Entries", "🚪 Logout"])

    if menu == "➕ Add Entry":
        st.subheader("Add Today's Progress")

        qname = st.text_input("Question Name")
        topic = st.text_input("Topic")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        status = st.selectbox("Status", ["Done", "Pending", "Revised"])
        submit = st.button("Submit Entry")

        if submit:
            today = date.today().strftime("%Y-%m-%d")
            add_entry(username, today, qname, topic, difficulty, status)
            st.success("Entry added successfully!")

    elif menu == "📋 View Entries":
        st.subheader("Your Progress Entries" if username.lower() != "aryan" else "All User Progress Entries")
        entries = fetch_entries(username)
        if entries:
            st.dataframe(entries, use_container_width=True)
        else:
            st.info("No entries found.")

    elif menu == "🚪 Logout":
        del st.session_state.username
        st.experimental_rerun()
