import streamlit as st
import sqlite3
from datetime import date

# ======= Setup Database Connection =======
conn = sqlite3.connect("aiml_tracker.db", check_same_thread=False)
cursor = conn.cursor()

# ======= Create Table If Not Exists =======
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

# ======= Functions =======
def add_entry(username, date, question_name, topic, difficulty, status):
    cursor.execute(
        "INSERT INTO progress (username, date, question_name, topic, difficulty, status) VALUES (?, ?, ?, ?, ?, ?)",
        (username, date, question_name, topic, difficulty, status)
    )
    conn.commit()

def fetch_entries(username):
    if username.lower() == "aryan":
        cursor.execute("SELECT * FROM progress ORDER BY date DESC")
    else:
        cursor.execute("SELECT * FROM progress WHERE username = ? ORDER BY date DESC", (username,))
    return cursor.fetchall()

# ======= Streamlit App =======
st.title("🧠 NeuroBolt AIML Progress Tracker")

# ---- Login ----
if 'username' not in st.session_state:
    st.subheader("🔐 Login")
    username_input = st.text_input("Enter your username")
    if st.button("Login"):
        if username_input.strip() != "":
            st.session_state.username = username_input.strip()
            st.success(f"Welcome {username_input}!")
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid username.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    username = st.session_state.username

    menu = st.sidebar.selectbox("📂 Menu", ["➕ Add Entry", "📋 View Entries", "🚪 Logout"])

    if menu == "➕ Add Entry":
        st.subheader("✍️ Add Today's Progress")

        qname = st.text_input("📝 Question Name")
        topic = st.text_input("📚 Topic")
        difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])
        status = st.selectbox("📌 Status", ["Done", "Pending", "Revised"])
        submit = st.button("✅ Submit Entry")

        if submit:
            if qname and topic:
                today = date.today().strftime("%Y-%m-%d")
                add_entry(username, today, qname, topic, difficulty, status)
                st.success("Entry added successfully!")
            else:
                st.error("Question name and topic are required.")

    elif menu == "📋 View Entries":
        st.subheader("📈 Your Progress" if username.lower() != "aryan" else "📊 All Users' Progress")
        entries = fetch_entries(username)
        if entries:
            st.dataframe(entries, use_container_width=True)
        else:
            st.info("No entries found yet.")

    elif menu == "🚪 Logout":
        del st.session_state.username
        st.experimental_rerun()

   
   
