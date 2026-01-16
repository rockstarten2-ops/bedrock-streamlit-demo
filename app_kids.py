import streamlit as st
import boto3
import json
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Duggu’s Learning Buddy",
    layout="centered"
)

# -----------------------------
# PREMIUM KID UI CSS
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #FAFAFA;
}
.chat-card {
    padding: 14px 18px;
    border-radius: 14px;
    margin-bottom: 10px;
    font-size: 16px;
    line-height: 1.4;
}
.user {
    background-color: #E3F2FD;
}
.bot {
    background-color: #FFF8E1;
}
.header {
    text-align: center;
    margin-bottom: 20px;
}
.stars {
    text-align: center;
    font-size: 18px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="header">
<h1>Hi Duggu! 👋</h1>
<h3>I’m your learning buddy 😊</h3>
<p>We’ll learn using games, stories, and fun questions!</p>
<p style="color:gray;">Created with love by your dad ❤️</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

# -----------------------------
# STAR DISPLAY
# -----------------------------
st.markdown(
    f"<div class='stars'>⭐ Stars earned: {st.session_state.stars}</div>",
    unsafe_allow_html=True
)

# -----------------------------
# BEDROCK CLIENT
# -----------------------------
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# -----------------------------
# DISPLAY CHAT (LIMIT SCROLL)
# -----------------------------
for msg in st.session_state.messages[-6:]:
    css = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-card {css}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# -----------------------------
# INPUT BOX (BOTTOM)
# -----------------------------
user_input = st.chat_input("Type your answer here 😊")

# -----------------------------
# HANDLE INPUT
# -----------------------------
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": f"🧒 {user_input}"
    })

    # Reward only AFTER child answers
    reward_text = ""
    if st.session_state.awaiting_answer:
        st.session_state.stars += 1
        reward_text = "\n\n⭐ You earned a star!"
        st.session_state.awaiting_answer = False

    # Rotate learning themes invisibly
    learning_modes = [
        "maths",
        "india_capitals",
        "se_asia_capitals",
        "rajasthan_history",
        "fun_quiz"
    ]
    selected_mode = random.choice(learning_modes)

    system_prompt = f"""
You are a learning buddy for a Grade 4 child named Duggu.

RULES:
- VERY short answers (1–3 sentences)
- Simple words
- Ask ONLY one question
- Friendly, playful tone
- No long explanations

LEARNING MODE (do not say this to child): {selected_mode}

KNOWLEDGE YOU CAN USE:
- Indian state capitals
- Southeast Asia capitals
- Rajasthan history stories (Prithviraj Chauhan, bravery, values)
- Basic maths and fun quizzes

If you ask a question, wait for Duggu’s answer.
"""

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": system_prompt + "\nChild says: " + user_input}
        ],
        "max_tokens": 140,
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

        if "?" in reply:
            st.session_state.awaiting_answer = True

        reply += reward_text

    except Exception:
        reply = "Oops 😅 Let’s try again!"

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🤖 {reply}"
    })
