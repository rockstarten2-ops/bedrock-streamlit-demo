import streamlit as st
import boto3
import json
import random

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Duggu’s Learning Buddy",
    layout="centered"
)

# ---------------------------------
# BASIC CLEAN UI
# ---------------------------------
st.markdown("""
<style>
body {
    background-color: #ffffff;
}
.chat {
    padding: 10px 0;
    font-size: 16px;
}
.user {
    margin-bottom: 10px;
}
.bot {
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# SIDEBAR (STARS ONLY)
# ---------------------------------
with st.sidebar:
    st.markdown("### ⭐ Rewards")
    if "stars" not in st.session_state:
        st.session_state.stars = 0
    st.markdown(f"**Stars earned:** {st.session_state.stars}")

# ---------------------------------
# HEADER
# ---------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:25px;">
<h1>Hi Duggu! 👋🐯</h1>
<h3>I’m your learning buddy 😊</h3>
<p>We’ll learn using games, stories, and fun questions!</p>
<p style="color:gray;">Created with love by your dad ❤️</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# SESSION STATE
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

# ---------------------------------
# DISPLAY CHAT (ORDER SAFE)
# ---------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat user'>🧒 <b>Duggu:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat bot'>🐯 <b>Buddy:</b> {msg['content']}</div>", unsafe_allow_html=True)

# ---------------------------------
# INPUT
# ---------------------------------
user_input = st.chat_input("Type your answer here 😊")

# ---------------------------------
# BEDROCK CLIENT
# ---------------------------------
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# ---------------------------------
# HANDLE INPUT (FIXED ORDER)
# ---------------------------------
if user_input:
    # 1️⃣ Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 2️⃣ Reward ONLY after child answers a question
    if st.session_state.awaiting_answer:
        st.session_state.stars += 1
        st.session_state.awaiting_answer = False

    # 3️⃣ Rotate learning internally
    learning_modes = [
        "maths",
        "india_capitals",
        "se_asia_capitals",
        "rajasthan_history",
        "fun_quiz"
    ]
    mode = random.choice(learning_modes)

    system_prompt = f"""
You are a fun, kind learning buddy for a Grade 4 child named Duggu.

RULES:
- Use Duggu’s name often
- 1–2 short sentences only
- Ask ONE question at a time
- Friendly, playful tone
- Simple words
- Never long explanations

LEARNING MODE (internal): {mode}

KNOWLEDGE:
- Indian state capitals
- Southeast Asia capitals
- Rajasthan history (Prithviraj Chauhan, bravery stories)
- Basic maths & fun quizzes

If you ask a question, wait for Duggu’s answer.
"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": system_prompt + "\nDuggu says: " + user_input
            }
        ],
        "max_tokens": 120,
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

        # Detect if bot asked a question
        if "?" in reply:
            st.session_state.awaiting_answer = True

    except Exception:
        reply = "Oops Duggu 😅 Let’s try again!"

    # 4️⃣ Save assistant reply immediately
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # 5️⃣ Force rerender (keeps order correct)
    st.rerun()
