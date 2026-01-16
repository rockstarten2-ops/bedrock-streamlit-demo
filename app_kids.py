import streamlit as st
import random

# ------------------ PAGE SETUP ------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🎒",
    layout="wide"
)

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "current_topic" not in st.session_state:
    st.session_state.current_topic = None

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "recent_questions" not in st.session_state:
    st.session_state.recent_questions = set()

# ------------------ DATA BANK ------------------
QUESTIONS = {
    "Maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 × 3?", "24"),
        ("What is 15 − 6?", "9"),
        ("What is half of 20?", "10"),
    ],
    "Science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is known as the King of the Jungle?", "lion"),
        ("What do plants need to make food?", "sunlight"),
    ],
    "Capitals": [
        ("What is the capital of India?", "delhi"),
        ("What is the capital of Maharashtra?", "mumbai"),
        ("Akola is in which Indian state?", "maharashtra"),
        ("What is the capital of Thailand?", "bangkok"),
    ],
    "Games": [
        ("Spell this backwards: CAT", "tac"),
        ("Which number comes next: 2, 4, 6, ?", "8"),
    ],
    "Stories": [
        ("Who was Maharana Pratap?", "king"),
        ("Prithviraj Chauhan was a brave king or a scientist?", "king"),
    ]
}

PRAISE = [
    "Awesome work, Duggu! 🌟",
    "High five! 🙌",
    "You're learning fast! 🚀",
    "Great thinking, buddy! 💪",
    "Nice job! 🎉"
]

ENCOURAGE = [
    "Nice try! Want a small hint? 😊",
    "No worries! Learning takes practice 💙",
    "Good effort! Let’s keep going 🚴‍♂️"
]

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("## 🎒 Duggu's Learning World")

    topic = st.radio(
        "Choose a topic",
        ["Maths", "Science", "Capitals", "Games", "Stories"],
        index=0 if st.session_state.current_topic is None else
        ["Maths", "Science", "Capitals", "Games", "Stories"].index(st.session_state.current_topic)
    )

    st.session_state.current_topic = topic

    st.markdown("---")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")
    st.info("💡 Ask anything!\nEven fun facts about Akola 😄")

# ------------------ HEADER ------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 🐯 Buddy")
st.caption("Created with love by your dad ❤️")

st.markdown("---")

# ------------------ CHAT DISPLAY ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ ASK QUESTION ------------------
def ask_question():
    topic = st.session_state.current_topic
    available = [
        q for q in QUESTIONS[topic]
        if q[0] not in st.session_state.recent_questions
    ]

    if not available:
        st.session_state.recent_questions.clear()
        available = QUESTIONS[topic]

    question, answer = random.choice(available)
    st.session_state.recent_questions.add(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🐯 **Buddy:** {random.choice(PRAISE)}\n\n{question}"
    })

    return answer

# ------------------ INITIAL QUESTION ------------------
if not st.session_state.messages:
    st.session_state.correct_answer = ask_question()

# ------------------ USER INPUT ------------------
user_input = st.chat_input("Type your answer 😊")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": f"🧒 **Duggu:** {user_input}"
    })

    # CHECK ANSWER
    if user_input.strip().lower() == st.session_state.correct_answer:
        st.session_state.stars += 1
        reply = f"🎉 {random.choice(PRAISE)} You earned ⭐ **1 star**!"
    else:
        reply = random.choice(ENCOURAGE)

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🐯 **Buddy:** {reply}"
    })

    st.session_state.question_count += 1

    # Ask to mix topics occasionally
    if st.session_state.question_count % 4 == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🐯 **Buddy:** Want to keep going or try a different topic? 😊"
        })
    else:
        st.session_state.correct_answer = ask_question()

    st.rerun()
