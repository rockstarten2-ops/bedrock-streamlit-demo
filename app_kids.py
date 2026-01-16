import streamlit as st
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Duggu’s Learning Buddy", layout="centered")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()

if "question_counter" not in st.session_state:
    st.session_state.question_counter = 0

if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 🎯 Topics")
    st.markdown("• Maths\n• Science\n• Capitals\n• Games\n• Stories")
    st.markdown("---")
    st.markdown(f"### ⭐ Stars Earned: {st.session_state.stars}")

# ---------------- HEADER ----------------
st.markdown("""
<div style="text-align:center;">
<h1>Hi Duggu! 👋🐯</h1>
<h3>I’m your learning buddy 😊</h3>
<p>We’ll learn using games, fun facts & stories!</p>
<p style="color:gray;">Created with love by your dad ❤️</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- QUESTION BANK ----------------
QUESTION_BANK = [
    ("What is 8 + 6?", "14"),
    ("What is 9 × 3?", "27"),
    ("Which planet is called the Red Planet?", "mars"),
    ("What is the capital of India?", "delhi"),
    ("What is the capital of Maharashtra?", "mumbai"),
    ("What is the capital of Rajasthan?", "jaipur"),
    ("Duggu, do you know which city is called the Pink City?", "jaipur"),
    ("Akola is in which Indian state?", "maharashtra"),
    ("Who was the brave king Prithviraj Chauhan?", "king"),
    ("Let’s play! Tell me a number between 1 and 10 😊", None),
]

def get_next_question():
    remaining = [q for q in QUESTION_BANK if q[0] not in st.session_state.asked_questions]
    if not remaining:
        st.session_state.asked_questions.clear()
        remaining = QUESTION_BANK
    return random.choice(remaining)

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧒 **Duggu:** {msg['content']}")
    else:
        st.markdown(f"🐯 **Buddy:** {msg['content']}")

# ---------------- INPUT ----------------
user_input = st.chat_input("Type your answer here 😊")

# ---------------- LOGIC ----------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check answer
    if st.session_state.awaiting_answer:
        correct = st.session_state.current_answer
        if correct and user_input.lower().strip() == correct:
            st.session_state.stars += 1
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎉 Great job Duggu! You earned ⭐ 1 star!"
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "😊 Nice try Duggu! Let’s keep learning together."
            })

        st.session_state.awaiting_answer = False

    # Ask new question
    q, ans = get_next_question()
    st.session_state.asked_questions.add(q)
    st.session_state.current_question = q
    st.session_state.current_answer = ans
    st.session_state.awaiting_answer = True
    st.session_state.question_counter += 1

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Duggu, here’s a fun one for you 😊\n\n{q}"
    })

    # Topic switch suggestion
    if st.session_state.question_counter % 3 == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Duggu, want to change topic or mix things up? 🎲 Maths, games, capitals, or stories?"
        })

    st.rerun()
