import streamlit as st
import boto3
import json
import random

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Duggu’s Learning Buddy",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS (Premium Kid UI)
# -------------------------------
st.markdown("""
<style>
.chat-message {
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    font-size: 16px;
}
.user-msg {
    background-color: #E3F2FD;
}
.bot-msg {
    background-color: #FFF8E1;
}
.sidebar-box {
    background-color: #FCE4EC;
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR – LEARNING MODES
# -------------------------------
st.sidebar.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
st.sidebar.title("🎒 Choose a learning game")

topic = st.sidebar.radio(
    "What do you want to play today?",
    [
        "🧮 Maths Fun",
        "🍕 Fractions Game",
        "🇮🇳 India State Capitals",
        "🌏 SE Asia Capitals",
        "🏰 Rajasthan History Stories",
        "🎉 Fun Quiz"
    ]
)

st.sidebar.markdown("---")

if "stars" not in st.session_state:
    st.session_state.stars = 0

st.sidebar.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<h1>Hi Duggu! 👋</h1>
<h3>I’m your learning buddy 🤖</h3>
<p>We’ll learn using games, stories, and fun questions!</p>
<p style="color:gray;">Created with love by your dad ❤️</p>
<hr>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

# -------------------------------
# BEDROCK CLIENT
# -------------------------------
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# -------------------------------
# DISPLAY CHAT (LIMITED)
# -------------------------------
for msg in st.session_state.messages[-6:]:
    css = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(
        f"<div class='chat-message {css}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# -------------------------------
# CHAT INPUT
# -------------------------------
user_input = st.chat_input("Ask me something fun 😊")

# -------------------------------
# HANDLE INPUT
# -------------------------------
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": f"🧒 {user_input}"
    })

    # ⭐ Reward logic ONLY AFTER child answers
    if st.session_state.awaiting_answer:
        st.session_state.stars += 1
        reward_text = "\n\n⭐ You earned a star!"
        st.session_state.awaiting_answer = False
    else:
        reward_text = ""

    # -------------------------------
    # SYSTEM PROMPT (STRICT)
    # -------------------------------
    system_prompt = f"""
You are a learning buddy for a Grade 4 child named Duggu.

RULES:
- Keep answers SHORT (2–3 sentences)
- Use simple words
- Ask ONLY ONE question
- Be fun and encouraging
- No long explanations
- Topic: {topic}

SPECIAL KNOWLEDGE:
- India state capitals
- Southeast Asia country capitals
- Rajasthan history stories (Prithviraj Chauhan, Rajput bravery)
- Maths basics

If this is a quiz question, wait for Duggu’s answer before rewarding.
"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": system_prompt + "\n\nChild says: " + user_input}
        ],
        "max_tokens": 180,
        "temperature": 0.6
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        reply = json.loads(response["body"].read())["content"][0]["text"]

        # If bot asks a question → wait for answer
        if "?" in reply:
            st.session_state.awaiting_answer = True

        reply += reward_text

    except Exception:
        reply = "Oops 😅 Let’s try again!"

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🤖 {reply}"
    })
