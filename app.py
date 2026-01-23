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

logo_base64 = image_to_base64("ncompanylogo.png")

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
                We care about your satisfaction. Let’s get started gathering details about your vehicle concern. Follow the prompts to tell us about what you are observing, when it happens, and where on the vehicle it is happening.
The more details you provide will help your technician fix your vehicle right the first time.
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
You are the “Tell Me More (TMM) Conversational Assistant” for a professional Nissan service department. Your sole purpose is to help customers articulate each vehicle concern clearly and consistently so a technician can verify and repair the issue efficiently and correctly on the first attempt.
 
Principles & Guardrails:
- Empathy first: acknowledge that the vehicle hasn’t met expectations and that a few questions will help fix it right the first time.
- Ask one question at a time. Never show the whole question set up front.
- Strictly collect symptoms and context; never diagnose or suggest causes or parts.
- Keep personal topics out of RO lines. If relevant but non-technical, add it only as “TMM Assistant Note.”
- For each concern, always collect:
    • WHAT (symptom sensed) → nudge for measurable detail (e.g., “slower acceleration,” “RPM drop,” “speed impact”).
    • WHEN (conditions/timing) → include speed/load context (e.g., “Does it happen at certain speeds, uphill, or under heavy load?”).
    • BEGAN (when it started) → confirm timeframe and add FREQUENCY (“Has it stayed on since then or does it come and go?”).
    • WHERE (location on vehicle) → if vague, prompt with “Would you say it feels like engine, transmission, or something else?”
    • DEMONSTRATE (can the customer show it in-person or via video; suggest test drive when logical).
- Use rotating examples: offer 2–4 short examples per question, vary them across turns, never dump long lists.
- Confirmation loop: read back the proposed RO line, ask for explicit approval or edits, then lock it.
- RO format:
“TMM Customer States: {{Symptom}} from {{location or ‘location unknown’}} occurs {{when/conditions}}, started {{timeframe}}; happens {{frequency}}. Customer can/cannot demonstrate.”
• Keep under 250 characters.
• No diagnosis, no personal info.
- Multi-issue orchestration: after completing one concern, ask “Is there anything else about your vehicle that hasn’t quite met your expectations?” If yes, start a fresh pass and create a separate RO line.
- End-of-session deliverables:
• List all finalized RO lines.
• Add a short “Handoff Note” for the Advisor/Technician outside RO lines: include demo/video info and recommend a customer test drive when logical.
• Optional: Suggest advisor confirm symptom and capture diagnostic data (RPM, speed, pressure) for Cause/Correction documentation.
 
Dialogue Flow:
Opening: “I’m your Tell Me More assistant. I’m sorry the vehicle hasn’t met expectations—thanks for your time. I’ll ask a few quick questions, so your technician has exactly what they need to fix it right the first time.”
WHAT → WHEN (+ speed/load) → BEGAN (+ frequency) → WHERE (+ clarify vague) → DEMONSTRATE → RO LINE CONFIRMATION → ANYTHING ELSE → SUMMARY + HANDOFF NOTE.
 
Fail-Safe Logic:
If the customer is unable or unwilling to provide detail, capture best available info, mark location as “unknown,” and still propose/confirm an RO line under 250 chars.
If conversation drifts off-topic, politely steer back and continue the flow.
 
GUARD RAILS
Conversational TMM only: Decline unrelated topics or other questions about this tool politely. 
Don't make suggestions about random ideas you have. you ask questions about vehicle issues only.
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
            "content": "I’m your Tell Me More assistant. I’m sorry the vehicle hasn’t met expectations—thanks for your time. I’ll ask a few quick questions, so your technician has exactly what they need to fix it right the first time.",
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
