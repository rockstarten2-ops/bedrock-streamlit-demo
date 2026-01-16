import streamlit as st
import boto3
import json

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Duggu's Learning Buddy",
    page_icon="📘",
    layout="centered"
)

# ===============================
# Header
# ===============================
st.markdown(
    """
    <h1>Hi Duggu! 👋</h1>
    <h3>I'm your learning buddy 🤓</h3>
    <p>Ask me a question or choose a topic below. We'll learn together!</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ===============================
# Sidebar (Topics)
# ===============================
st.sidebar.header("📚 Choose a topic")

topics = [
    "Maths ➕",
    "Fractions 🍕",
    "Multiplication ✖️",
    "Division ➗",
    "Science 🔬",
    "Reading 📖",
    "Fun Quiz 🎉"
]

selected_topic = st.sidebar.radio("What do you want to learn today?", topics)

# ===============================
# Initialize session state
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# Show chat history
# ===============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# Topic starter message
# ===============================
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Awesome choice, Duggu! 😄 Let’s learn **{selected_topic}**. What would you like to start with?"
    })
    st.rerun()

# ===============================
# Chat input (BOTTOM like ChatGPT)
# ===============================
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ===============================
    # Bedrock client
    # ===============================
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    # ===============================
    # Build Claude 3 messages (CORRECT FORMAT)
    # ===============================
    messages = []
    for m in st.session_state.messages:
        messages.append({
            "role": m["role"],
            "content": [
                {"type": "text", "text": m["content"]}
            ]
        })

    # ===============================
    # Invoke Claude 3 Sonnet
    # ===============================
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "system": (
                "You are a friendly, patient learning buddy for a Grade 4 student named Duggu. "
                "Use very simple language. Explain step by step. "
                "Use examples, emojis, and encouragement. "
                "Never use advanced terms. Ask small follow-up questions."
            ),
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.5
        })
    )

    result = json.loads(response["body"].read())
    assistant_reply = result["content"][0]["text"]

    # ===============================
    # Show assistant response
    # ===============================
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

# ===============================
# Footer
# ===============================
st.markdown(
    """
    <hr>
    <center>
        <p style="color: gray;">
            🤖 Created with love by your dad ❤️
        </p>
    </center>
    """,
    unsafe_allow_html=True
)
