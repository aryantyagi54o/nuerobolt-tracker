import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

# ======================
# Database Setup
# ======================
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

# ======================
# Database Functions
# ======================
def insert_entry(date_val, question, topic, status, remarks, mock, revision):
    cursor.execute('''
        INSERT INTO progress (date, question_name, topic, status, remarks, mock_test, revision_done)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date_val, question, topic, status, remarks, mock, revision))
    conn.commit()

def fetch_entries():
    cursor.execute("SELECT date, question_name, topic, status, remarks, mock_test, revision_done FROM progress ORDER BY id DESC")
    return cursor.fetchall()

# ======================
# Streamlit GUI
# ======================
st.set_page_config("NeuroBolt Tracker", layout="centered", page_icon="🧠")
st.markdown("<h1 style='text-align:center; color:#2d3436;'>🧠 NeuroBolt Coding Tracker</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# === Form ===
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        date_val = st.date_input("📅 Date", date.today())
        question = st.text_input("📝 Question Name")
        topic = st.text_input("📚 Topic")
    with col2:
        status = st.selectbox("⏳ Status", ["✅ Completed", "⏳ In Progress", "❌ Not Done"])
        remarks = st.text_area("🗒️ Remarks", height=80)
        mock = st.checkbox("✅ Mock Test Done")
        revision = st.checkbox("🔁 Revision Done")

    submitted = st.form_submit_button("💾 Save Entry")

    if submitted:
        if not question or not topic:
            st.warning("⚠️ Question Name and Topic are required.")
        else:
            insert_entry(str(date_val), question, topic, status, remarks, int(mock), int(revision))
            st.success("✅ Progress saved successfully!")

# === Table ===
st.markdown("### 📊 Progress Table")
records = fetch_entries()

if records:
    df = pd.DataFrame(records, columns=["Date", "Question", "Topic", "Status", "Remarks", "Mock", "Revision"])
    df["Mock"] = df["Mock"].map({1: "Yes", 0: "No"})
    df["Revision"] = df["Revision"].map({1: "Yes", 0: "No"})
    st.dataframe(df, use_container_width=True)
else:
    st.info("🗃️ No records found. Add your first entry above.")

# === Footer ===
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:gray;'>🧠 Built with ❤️ by Aryan — NeuroBolt Tracker</div>", unsafe_allow_html=True)
