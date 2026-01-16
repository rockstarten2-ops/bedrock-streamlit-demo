import streamlit as st
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Duggu’s Learning World",
    page_icon="🦁",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "current_answer" not in st.session_state:
    st.session_state.current_answer = None

if "asked" not in st.session_state:
    st.session_state.asked = set()

# -----------------------------
# QUESTION STARTERS (NOT LIMITS)
# -----------------------------
QUESTION_SEEDS = {
    "Maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 + 7?", "15"),
        ("What is 12 × 2?", "24"),
    ],
    "Science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is known as the King of the Jungle?", "lion"),
    ],
    "Capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
        ("What is the capital of Thailand?", "bangkok"),
    ],
    "Stories": [
        ("Do you want to hear a brave story about Prithviraj Chauhan?", None),
    ]
}

# -----------------------------
# CHAT HELPERS (NO STREAMLIT CHAT)
# -----------------------------
def buddy(text):
    st.session_state.chat.append(f"🦁 **Buddy:** {text}")

def duggu(text):
    st.session_state.chat.append(f"🧒 **Duggu:** {text}")

def ask_question(topic):
    pool = [
        q for q in QUESTION_SEEDS.get(topic, [])
        if q[0] not in st.session_state.asked
    ]

    if not pool:
        buddy("You’re doing awesome, Duggu! 🌟 Ask me anything or choose another topic.")
        return

    q, ans = random.choice(pool)
    st.session_state.asked.add(q)
    st.session_state.current_answer = ans
    buddy(f"Hey Duggu 😊 {q}")

# -----------------------------
# SIDEBAR (CLEAN, CLICKABLE)
# -----------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"### ⭐ Stars Earned: **{st.session_state.stars}**")
    st.markdown("---")

    if st.button("➕ Maths"):
        buddy("Maths time! Let’s have fun with numbers 🎯")
        ask_question("Maths")

    if st.button("🔬 Science"):
        buddy("Science is awesome! 🔭 Let’s explore")
        ask_question("Science")

    if st.button("🌍 Capitals"):
        buddy("Let’s travel the world, Duggu ✈️")
        ask_question("Capitals")

    if st.button("📖 Stories"):
        buddy("Story time! 📜 Ready for a brave tale?")
        ask_question("Stories")

    st.markdown("---")
    st.caption("Ask anything — even fun facts about Akola 😊")

# -----------------------------
# MAIN HEADER
# -----------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.markdown("We’ll learn with games, stories, and fun questions!")
st.markdown("_Created with love by your dad ❤️_")
st.markdown("---")

# -----------------------------
# CHAT DISPLAY
# -----------------------------
for line in st.session_state.chat:
    st.markdown(line)

# -----------------------------
# USER INPUT (SINGLE FLOW)
# -----------------------------
user_input = st.text_input("Type here 😊", key="input")

if user_input:
    duggu(user_input)

    if st.session_state.current_answer is not None:
        if user_input.strip().lower() == st.session_state.current_answer:
            st.session_state.stars += 1
            buddy("🎉 Fantastic, Duggu! You earned ⭐ 1 star!")
        else:
            buddy("Nice try, Duggu 💪 That was a tricky one!")

        st.session_state.current_answer = None

    else:
        buddy(
            "That’s a great thought, Duggu 😄 "
            "You can ask me questions, play games, or click a topic!"
        )

    st.rerun()
