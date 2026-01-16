import streamlit as st
import boto3
import json
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Duggu’s Learning Buddy", layout="centered")

# -----------------------------
# STYLES (CLEAN & PREMIUM)
# -----------------------------
st.markdown("""
<style>
.chat { margin-bottom: 12px; font-size: 16px; }
.user { }
.bot { }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "current_topic" not in st.session_state:
    st.session_state.current_topic = "Maths"

if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

if "last_correct" not in st.session_state:
    st.session_state.last_correct = None

# -----------------------------
# SIDEBAR (SIMPLE & CLEAN)
# -----------------------------
with st.sidebar:
    st.markdown("### 🎯 Choose a topic")
    st.session_state.current_topic = st.radio(
        "",
        ["Maths", "Science", "Capitals", "Fun Games", "Stories"]
    )
    st.markdown("---")
    st.markdown(f"### ⭐ Stars Earned: {st.session_state.stars}")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div style="text-align:center;">
<h1>Hi Duggu! 👋🐯</h1>
<h3>I’m your learning buddy 😊</h3>
<p>We’ll learn using games, fun facts, and stories!</p>
<p style="color:gray;">Created with love by your dad ❤️</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# SHOW CHAT
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat user'>🧒 <b>Duggu:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat bot'>🐯 <b>Buddy:</b> {msg['content']}</div>", unsafe_allow_html=True)

# -----------------------------
# INPUT
# -----------------------------
user_input = st.chat_input("Type your answer here 😊")

# -----------------------------
# BEDROCK
# -----------------------------
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# -----------------------------
# QUESTION GENERATOR (CONTROLLED)
# -----------------------------
def get_next_question(topic):
    if topic == "Maths":
        return random.choice([
            "What is 7 + 5?",
            "What is 6 × 4?",
            "What is 20 ÷ 5?"
        ])
    if topic == "Science":
        return random.choice([
            "Why do plants need sunlight?",
            "Which planet is called the Red Planet?",
            "What do we breathe in to stay alive?"
        ])
    if topic == "Capitals":
        return random.choice([
            "What is the capital of India?",
            "What is the capital of Maharashtra?",
            "What is the capital of Thailand?"
        ])
    if topic == "Fun Games":
        return "Let’s play! Tell me a number between 1 and 10 😊"
    if topic == "Stories":
        return "Duggu, do you want to hear a brave story from Rajasthan or a fun fact about Akola?"

# -----------------------------
# HANDLE INPUT
# -----------------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check correctness (simple heuristic)
    correct_answers = ["12", "24", "4", "delhi", "mumbai", "jaipur", "bangkok", "oxygen", "mars"]
    is_correct = user_input.lower().strip() in correct_answers

    if st.session_state.awaiting_answer:
        if is_correct:
            st.session_state.stars += 1
            feedback = "🎉 Great job Duggu! You earned ⭐ 1 star!"
        else:
            feedback = "😊 Nice try Duggu! Let’s learn together."

        st.session_state.messages.append({"role": "assistant", "content": feedback})
        st.session_state.awaiting_answer = False

    # Ask next question
    question = get_next_question(st.session_state.current_topic)
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Duggu, here’s a fun one for you 😊\n\n{question}"
    })
    st.session_state.awaiting_answer = True
    st.session_state.question_count += 1

    # Ask feedback every 5 questions
    if st.session_state.question_count % 5 == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Duggu, are you enjoying this? 👍 Fun / 😐 Okay / 👎 Boring"
        })

    st.rerun()
