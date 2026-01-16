import streamlit as st
import boto3
import json
import random

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Duggu's Learning Buddy",
    layout="wide"
)

# --------------------------------
# SIDEBAR – TOPIC SELECTION
# --------------------------------
st.sidebar.title("🎒 Choose a topic")
topic = st.sidebar.radio(
    "What do you want to learn today?",
    ["Maths ➕", "Fractions 🍕", "Multiplication ✖️", "Division ➗", "Science 🔬", "Reading 📖", "Fun Quiz 🎉"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("⭐ **Reward Stars:**")

if "stars" not in st.session_state:
    st.session_state.stars = 0

st.sidebar.markdown(f"🌟 **{st.session_state.stars} stars**")

# --------------------------------
# HEADER
# --------------------------------
st.markdown(
    """
    <h1>Hi Duggu! 👋</h1>
    <h3>I’m your learning buddy 🤖</h3>
    <p>Ask me anything you’re learning in school. We’ll figure it out together!</p>
    <p style="font-size:14px; color:gray;">Created with love by your dad ❤️</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --------------------------------
# SESSION STATE
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_topic" not in st.session_state:
    st.session_state.current_topic = topic

# --------------------------------
# AUTO MESSAGE WHEN TOPIC CHANGES
# --------------------------------
if topic != st.session_state.current_topic:
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Great choice, Duggu! 🎉 Let’s learn **{topic}**. What would you like to try first?"
    })
    st.session_state.current_topic = topic

# --------------------------------
# DISPLAY CHAT (LAST 6 MESSAGES ONLY)
# --------------------------------
for msg in st.session_state.messages[-6:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------
# USER INPUT (CHATGPT STYLE)
# --------------------------------
user_input = st.chat_input("Ask me something fun 😊")

# --------------------------------
# BEDROCK CLIENT
# --------------------------------
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# --------------------------------
# HANDLE USER INPUT
# --------------------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # SYSTEM PROMPT – VERY IMPORTANT
    system_prompt = (
        "You are a fun learning buddy for a Grade 4 student named Duggu. "
        "Keep answers SHORT (2–4 simple sentences). "
        "Use very simple words. "
        "Ask only ONE question at the end. "
        "Avoid long explanations unless Duggu asks for more. "
        f"Current topic: {topic}. "
        "Make learning playful and easy."
    )

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": f"{system_prompt}\n\nQuestion: {user_input}"}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response["body"].read())
        bot_reply = response_body["content"][0]["text"]

        # ⭐ Reward stars randomly (fun + motivating)
        earned = random.choice([0, 1])
        if earned:
            st.session_state.stars += 1
            bot_reply += "\n\n⭐ You earned a star!"

    except Exception:
        bot_reply = "Oops! 😅 Something went wrong. Let’s try again!"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
