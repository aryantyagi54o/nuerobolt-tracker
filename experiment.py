import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

# ================================
# 💽 SQLite DB Setup
# ================================
conn = sqlite3.connect("aiml_tracker.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        question_name TEXT,
        topic TEXT,
        status TEXT,
        remarks TEXT,
        mock_test INTEGER,
        revision_done INTEGER
    )
''')
conn.commit()

# ================================
# 📦 DB Functions
# ================================
def save_entry(date_val, question, topic, status, remarks, mock, revision):
    cursor.execute('''
        INSERT INTO progress (date, question_name, topic, status, remarks, mock_test, revision_done)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date_val, question, topic, status, remarks, mock, revision))
    conn.commit()

def fetch_all():
    cursor.execute("SELECT date, question_name, topic, status, remarks, mock_test, revision_done FROM progress ORDER BY id DESC")
    return cursor.fetchall()

# ================================
# 🌐 Streamlit UI
# ================================
st.set_page_config(page_title="NeuroBolt Tracker", page_icon="🧠", layout="centered")
st.title("🧠 NeuroBolt Coding Tracker")

# --- Form Section ---
with st.form("entry_form"):
    st.subheader("📋 Fill New Entry")
    
    col1, col2 = st.columns(2)
    with col1:
        date_val = st.date_input("📅 Date", date.today())
        question = st.text_input("📝 Question Name")
        topic = st.text_input("📚 Topic")
    with col2:
        status = st.selectbox("⏳ Status", ["✅ Completed", "⏳ In Progress", "❌ Not Done"])
        remarks = st.text_area("🗒️ Remarks", height=90)
        mock = st.checkbox("✅ Mock Test Done")
        revision = st.checkbox("🔁 Revision Done")

    submitted = st.form_submit_button("💾 Save Progress")

    if submitted:
        if not question or not topic or not status:
            st.warning("⚠️ Please fill in all required fields.")
        else:
            save_entry(str(date_val), question, topic, status, remarks, int(mock), int(revision))
            st.success("✅ Progress saved successfully!")

# --- Display Section ---
st.markdown("---")
st.subheader("📊 Your Coding Progress")

data = fetch_all()
if data:
    df = pd.DataFrame(data, columns=["Date", "Question", "Topic", "Status", "Remarks", "Mock Test", "Revision"])
    df["Mock Test"] = df["Mock Test"].map({1: "Yes", 0: "No"})
    df["Revision"] = df["Revision"].map({1: "Yes", 0: "No"})
    st.dataframe(df, use_container_width=True)
else:
    st.info("🗂️ No records yet. Add your first entry above.")

# --- Footer ---
st.markdown("<br><center><sub>🚀 Built by Bhai for Aryan — NeuroBolt Tracker</sub></center>", unsafe_allow_html=True)
