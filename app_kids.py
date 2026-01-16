import streamlit as st
import boto3
import json

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Duggu's Learning Buddy",
    layout="centered"
)

# ===============================
# Header UI
# ===============================
st.title("Hi Duggu! 👋")
st.subheader("I’m your learning buddy 🤖")
st.markdown(
    "Ask me a question or tell me what you're learning in school. "
    "We’ll figure it out together!"
)

st.divider()

# ===============================
# Bedrock Client (UNCHANGED MODEL)
# ===============================
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# ===============================
# System Prompt (Grade 4 Persona)
# ===============================
SYSTEM_PROMPT = """
You are a friendly learning helper for a Grade 4 student named Duggu.

Rules:
- Use simple words and short sentences.
- Explain things step by step.
- Ask Aarav questions to help him think.
- Be kind, patient, and encouraging.
- Never make Aarav feel bad for mistakes.

Learning rules:
- Do NOT just give homework answers.
- Give hints and examples instead.
- Ask questions like "What do you think?" or "Let’s try together."

Safety rules:
- Only kid-friendly topics.
- No adult, violent, or scary content.
- No medical or personal advice.

You are Aarav’s learning buddy, not a strict teacher.
"""

# ===============================
# Session State
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# User Input
# ===============================
user_input = st.text_input(
    "What would you like help with today?",
    placeholder="Math, reading, science, or a question..."
)

# ===============================
# Call Claude Sonnet
# ===============================
def call_claude(user_message):
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "max_tokens": 500,
        "temperature": 0.5
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
        contentType="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]

# ===============================
# Handle Conversation
# ===============================
if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking... 🤔"):
        assistant_reply = call_claude(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# ===============================
# Display Chat History
# ===============================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Aarav:** {msg['content']}")
    else:
        st.markdown(f"**🤖 BuddyBot:** {msg['content']}")
