import streamlit as st
import boto3
import json

BUSINESS_NAME = "Tell Me More"
TAGLINE = "AI Assistant for Sales, Service & Product Intelligence"

st.set_page_config(page_title=BUSINESS_NAME, layout="centered")
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
/* Hide Streamlit default header */
header { visibility: hidden; }

/* Page background */
.main {
    background-color: #ffffff;
}

/* Brand title */
.brand-title {
    font-size: 38px;
    font-weight: 800;
    color: #0A2540; /* Deep automotive blue */
    margin-bottom: 4px;
}

/* Tagline */
.brand-tagline {
    font-size: 16px;
    color: #5b6777;
    margin-bottom: 24px;
}

/* Chat bubbles */
.stChatMessage[data-testid="user"] {
    background-color: #F0F4F8;
    border-radius: 12px;
}

.stChatMessage[data-testid="assistant"] {
    background-color: #E6EEF7;
    border-radius: 12px;
}

/* Input box */
textarea {
    border-radius: 10px !important;
}

/* Footer note */
.demo-note {
    font-size: 12px;
    color: #8a8f98;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

import base64

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = image_to_base64("nissaninfinitilogo.png")

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:24px;">
        <img src="data:image/png;base64,{logo_base64}" style="height:56px;" />
        <div>
            <div style="font-size:34px; font-weight:800;">Tell Me More</div>
            <div style="color:#6b7280;"> We’ll ask a few questions to understand what’s going on, so your dealership can prepare before your visit.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# st.image("nissaninfinitilogo.png", width=120)
# st.markdown(
#     f"""
#     <div style="
#         font-size:38px;
#         font-weight:800;
#         color:#0A2540;
#         margin-bottom:4px;
#     ">
#         {BUSINESS_NAME}
#     </div>
#     <div style="
#         font-size:16px;
#         color:#5b6777;
#         margin-bottom:24px;
#     ">
#       We’ll ask a few questions to understand what’s going on, so your dealership can prepare before your visit.
#     </div>
#     """,
#     unsafe_allow_html=True
# )

st.divider()

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


prompt = st.chat_input("""Start by telling us what you’re experiencing:

- 🚨 A warning light came on — tell me which one and when it started  
- 🔊 There’s a noise while driving or braking  
- 🔋 The vehicle struggles to start or loses charge  
- 🌡️ The engine feels hotter than usual  
- 🛠️ Something feels off, but I’m not sure how to describe it
""")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [
            {"role": "user", "content": f"""You are a Vehicle Service Intake Agent for an automotive manufacturer and its authorized dealerships.

Your sole responsibility is to gather clear, structured, and concise information about a customer’s vehicle issue BEFORE their dealership visit, so the service advisor can be prepared in advance.

You are NOT a general assistant, NOT a diagnostic tool, and NOT a repair advisor.

STRICT BEHAVIOR RULES (MUST FOLLOW):
1. Ask ONLY ONE question at a time.
2. Keep each question SHORT and focused (maximum 1 sentence).
3. NEVER repeat your role, introduction, or purpose after the first response.
4. NEVER reset the conversation or ask the user to “start over.”
5. NEVER ask long, multi-part, or numbered questions.
6. NEVER speculate, diagnose, recommend repairs, or mention costs.
7. NEVER mention AI, models, systems, or internal processes.
8. Do NOT provide explanations unless explicitly asked.
9. Maintain a professional, calm, dealership-style tone.

CONVERSATION STYLE:
- Be concise and polite.
- Acknowledge the user’s last answer briefly (1 short phrase max).
- Then ask the next most relevant follow-up question.
- Avoid unnecessary words.

INTAKE OBJECTIVE:
You are collecting the following information over multiple turns:
- Type of issue (warning light, noise, performance, starting, other)
- Timing (when it occurs)
- Frequency (constant, intermittent)
- Driving conditions (speed, braking, acceleration, weather, road)
- Severity indicators (loss of power, safety warnings, drivability issues)
- Any related symptoms

QUESTION FLOW RULES:
- Ask follow-up questions based ONLY on what the user just said.
- If the user gives a vague answer, ask for clarification with a short prompt.
- If the user gives a clear answer, move forward to the next logical detail.
- Do NOT jump ahead or ask unrelated questions.

END GOAL:
By the end of the conversation, the collected information should be sufficient for a dealership service advisor to understand the issue before the customer arrives.

If the user says something outside vehicle issues, gently redirect them back to describing the vehicle problem with a short question.

You must strictly follow these rules at all times."""
f"{prompt}"          
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    reply = result["content"][0]["text"]

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
