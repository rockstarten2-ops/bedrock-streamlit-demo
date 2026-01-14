import streamlit as st
import boto3
import json
import base64

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Tell Me More", layout="centered")

# ==============================
# Helper: Load image
# ==============================
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = image_to_base64("Novadrive.jpg",width=180)

# ==============================
# Header UI (UNCHANGED STYLE)
# ==============================
st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
        <img src="data:image/png;base64,{logo_base64}" style="height:55px;" />
        <div>
            <div style="font-size:32px; font-weight:800;">Tell Me More</div>
            <div style="color:#6b7280;">
                We’ll ask a few questions to understand what’s going on, so your dealership can prepare before your visit.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Bedrock client
# -----------------------------
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# -----------------------------
# System prompt (Claude rules)
# -----------------------------
SYSTEM_PROMPT = """
You are a vehicle service intake assistant for a Nissan/Infiniti dealership.

Rules you MUST follow:
- Be empathetic and human.
- Ask ONLY ONE short question at a time.
- Never repeat introductions.
- Never ask multi-part or long questions.
- Do NOT diagnose problems.
- Do NOT estimate costs.
- Do NOT suggest repairs.
- Acknowledge what the customer said before asking the next question.
- Use simple, conversational language.
-At the end of the conversation, provide a brief summary of the customer's described issue and the scheduled visit using only the customer's own words. Do not add diagnoses, causes, or recommendations. Ask the customer to confirm the summary.
"""

# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    # IMPORTANT:
    # Assistant greeting is UI-only (NOT sent to Bedrock)
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Start by telling me what you’re experiencing with your vehicle.",
        }
    ]

# -----------------------------
# Render chat history (UI only)
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Start by telling us what you’re experiencing:")

if user_input:
    # Show user message immediately
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------
    # Build Claude messages
    # IMPORTANT RULE:
    # First message sent to Claude MUST be from user
    # -----------------------------
    claude_messages = []

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            claude_messages.append(
                {
                    "role": "user",
                    "content": [{"type": "text", "text": msg["content"]}],
                }
            )
        elif msg["role"] == "assistant" and claude_messages:
            # Only add assistant messages AFTER at least one user message
            claude_messages.append(
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": msg["content"]}],
                }
            )

    # -----------------------------
    # Call Bedrock
    # -----------------------------
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "system": SYSTEM_PROMPT,
                "messages": claude_messages,
                "max_tokens": 300,
            }
        ),
        accept="application/json",
        contentType="application/json",
    )

    result = json.loads(response["body"].read())
    assistant_reply = result["content"][0]["text"]

    # -----------------------------
    # Save + display assistant reply
    # -----------------------------
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    with st.chat_message("assistant"):
        st.write(assistant_reply)
