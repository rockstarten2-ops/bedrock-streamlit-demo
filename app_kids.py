import streamlit as st
import boto3
import json
import random

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Hi Duggu!",
    page_icon="🧠",
    layout="centered"
)

# ---------------------------
# SESSION STATE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "turns" not in st.session_state:
    st.session_state.turns = 0

# ---------------------------
# AWS BEDROCK CLIENT
# ---------------------------
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# ---------------------------
# PHRASES (VARIETY!)
# ---------------------------
ENCOURAGEMENTS = [
    "Awesome thinking, Duggu! 🌟",
    "You’re doing great, buddy! 💪",
    "Nice try, Duggu! 😄",
    "Learning champ! 🏆",
    "High five, Duggu! ✋"
]

TRY_AGAIN = [
    "That’s okay! Want a hint or try something else?",
    "Good effort! Let’s keep learning together 😊",
    "No worries at all — learning is about trying!"
]

CHANGE_TOPIC_PROMPTS = [
    "Want to switch topics or keep going?",
    "Should we mix things up now?",
    "What would you like to try next?"
]

# ---------------------------
# QUESTION BANK
# ---------------------------
QUESTIONS = [
    # Maths
    {"q": "What is 8 + 7?", "a": "15"},
    {"q": "What is 12 × 2?", "a": "24"},

    # Science
    {"q": "Which planet is called the Red Planet?", "a": "mars"},
    {"q": "What gas do plants breathe in?", "a": "carbon dioxide"},

    # Capitals
    {"q": "What is the capital of India?", "a": "new delhi"},
    {"q": "Akola is in which Indian state?", "a": "maharashtra"},
    {"q": "What is the capital of Rajasthan?", "a": "jaipur"},
    {"q": "What is the capital of Thailand?", "a": "bangkok"},

    # Stories / History
    {
        "q": "Who was Prithviraj Chauhan?",
        "a": "king"
    },

    # Fun
    {
        "q": "Which animal is known as the King of the Jungle?",
        "a": "lion"
    }
]

# ---------------------------
# FUNCTIONS
# ---------------------------
def ask_new_question():
    q = random.choice(QUESTIONS)
    st.session_state.question = q["q"]
    st.session_state.answer = q["a"]

    intro = random.choice(ENCOURAGEMENTS)
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"{intro}\n\n{q['q']}"
    })

def evaluate_answer(user_input):
    correct = st.session_state.answer.lower() in user_input.lower()

    if correct:
        st.session_state.stars += 1
        response = f"🎉 Great job Duggu! You earned ⭐ 1 star!"
    else:
        response = random.choice(TRY_AGAIN)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.turns += 1

    # Occasionally ask to change topic
    if st.session_state.turns % 3 == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": random.choice(CHANGE_TOPIC_PROMPTS)
        })
    else:
        ask_new_question()

# ---------------------------
# SIDEBAR (CLEAN & PREMIUM)
# ---------------------------
with st.sidebar:
    st.markdown("## 🗺️ Duggu’s Learning World")
    st.markdown("""
    🔢 Maths  
    🔬 Science  
    🌍 Capitals  
    🎮 Games  
    📖 Stories  
    """)

    st.markdown("---")
    st.markdown("## ⭐ Stars Earned")
    st.markdown(f"### {st.session_state.stars} ⭐")

    if st.session_state.stars >= 5:
        st.success("🏅 Star Learner!")
    if st.session_state.stars >= 10:
        st.success("🏆 Super Smart Duggu!")

    st.markdown("---")
    st.info("Ask anything — even fun facts about Akola 😄")

# ---------------------------
# HEADER
# ---------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.caption("We’ll learn using games, stories, and fun questions!")
st.caption("Created with love by your dad ❤️")

st.markdown("---")

# ---------------------------
# CHAT DISPLAY
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.chat_input("Type your answer here 😊")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": f"Duggu: {user_input}"
    })

    if st.session_state.question is None:
        ask_new_question()
    else:
        evaluate_answer(user_input)
