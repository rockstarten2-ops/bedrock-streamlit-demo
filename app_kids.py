import streamlit as st
import boto3
import json

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Hi Duggu! 👋",
    page_icon="🎒",
    layout="wide"
)

# =========================
# Bedrock Client
# =========================
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "topic" not in st.session_state:
    st.session_state.topic = "Maths"

# =========================
# Sidebar (NO CHAT LOGIC)
# =========================
with st.sidebar:
    st.markdown("## 🎯 Choose a topic")
    topic = st.radio(
        "",
        ["Maths ➕", "Fractions 🍕", "Multiplication ✖️", "Division ➗", "Science 🔬", "Reading 📘", "Fun Quiz 🎉"]
    )
    st.session_state.topic = topic.split(" ")[0]

# =========================
# Header
# =========================
st.markdown(
    """
    <div style="text-align:center;">
        <h1>Hi Duggu! 👋</h1>
        <h3>I’m your learning buddy 🤖</h3>
        <p>Ask me anything you’re learning in school. We’ll figure it out together!</p>
        <p><i>Created with love by your dad ❤️</i></p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# Show Chat History
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# Chat Input (BOTTOM)
# =========================
user_input = st.chat_input("Type your question here...")

# =========================
# Claude Call (STRICTLY SAFE)
# =========================
if user_input:

    # 1️⃣ Append USER message FIRST
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # 2️⃣ Build Claude messages (USER MUST BE LAST)
    claude_messages = []
    for msg in st.session_state.messages:
        if msg["role"] in ["user", "assistant"]:
            claude_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    system_prompt = (
        "You are a friendly, patient learning buddy for a Grade 4 student named Duggu. "
        "Use simple words, emojis, and step-by-step explanations. "
        f"The current topic is {st.session_state.topic}. "
        "Encourage Duggu and make learning fun."
    )

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "system": system_prompt,
                "messages": claude_messages,
                "max_tokens": 500
            })
        )

        result = json.loads(response["body"].read())
        assistant_reply = result["content"][0]["text"]

    except Exception as e:
        assistant_reply = "😕 Oops! Something went wrong. Please try again."

    # 3️⃣ Append ASSISTANT message AFTER response
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
