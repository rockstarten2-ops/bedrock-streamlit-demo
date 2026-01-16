import streamlit as st
import random

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🎒",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "current_topic" not in st.session_state:
    st.session_state.current_topic = "Maths"

if "last_question" not in st.session_state:
    st.session_state.last_question = None

# ---------------- QUESTION BANK ----------------
QUESTIONS = {
    "Maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 × 3?", "24"),
        ("What is half of 20?", "10"),
        ("What is 15 − 6?", "9"),
    ],
    "Science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is known as the King of the Jungle?", "lion"),
        ("What do plants need to make food?", "sunlight"),
    ],
    "Capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
        ("What is the capital of Maharashtra?", "mumbai"),
        ("What is the capital of Thailand?", "bangkok"),
    ],
    "Games": [
        ("Spell this backwards: CAT", "tac"),
        ("Which number comes next: 2, 4, 6, ?", "8"),
    ],
    "Stories": [
        ("Who was Maharana Pratap — a brave king or a singer?", "king"),
        ("Prithviraj Chauhan was a king or a scientist?", "king"),
    ],
}

PRAISE = [
    "Awesome job, Duggu! 🌟",
    "High five! 🙌",
    "You're doing great! 🚀",
    "Nice thinking, buddy! 😊",
    "Well done! 🎉"
]

ENCOURAGE = [
    "Nice try! Want to try another one? 😊",
    "That's okay — learning is about trying 💙",
    "Good effort! Let's keep going 🚴‍♂️"
]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🎒 Duggu's Learning World")

    def topic_link(label, topic):
        if st.button(label, use_container_width=True):
            st.session_state.current_topic = topic
            ask_new_question()
            st.rerun()

    topic_link("➕ Maths", "Maths")
    topic_link("🔬 Science", "Science")
    topic_link("🌍 Capitals", "Capitals")
    topic_link("🎮 Games", "Games")
    topic_link("📖 Stories", "Stories")

    st.markdown("---")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")
    st.info("💡 Ask anything!\nEven fun facts about Akola 😄")

# ---------------- HEADER ----------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 🐯 Buddy")
st.caption("Created with love by your dad ❤️")
st.markdown("---")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- ASK QUESTION ----------------
def ask_new_question():
    topic = st.session_state.current_topic
    pool = QUESTIONS[topic]

    question, answer = random.choice(pool)
    while question == st.session_state.last_question:
        question, answer = random.choice(pool)

    st.session_state.last_question = question
    st.session_state.correct_answer = answer

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🐯 **Buddy:** {random.choice(PRAISE)}\n\n{question}"
    })

# First question
if not st.session_state.messages:
    ask_new_question()

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Type your answer 😊")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": f"👦 **Duggu:** {user_input}"
    })

    if user_input.strip().lower() == st.session_state.correct_answer:
        st.session_state.stars += 1
        reply = f"{random.choice(PRAISE)} You earned ⭐ **1 star**!"
    else:
        reply = random.choice(ENCOURAGE)

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🐯 **Buddy:** {reply}"
    })

    ask_new_question()
    st.rerun()
