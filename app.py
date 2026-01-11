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

Your purpose is to gather clear, structured information about a vehicle issue before a dealership visit so the service team can prepare in advance.

You are not diagnosing, recommending repairs, or estimating costs.

CRITICAL BEHAVIOR RULES:
- Never repeat your role or purpose after your first response.
- Never ask the customer to describe the issue again once it has been stated.
- Never reset the conversation.
- Never ask permission to continue.
- Never explain what you cannot do unless explicitly asked.

CONVERSATION STYLE:
- Sound like a calm, experienced service advisor.
- Use brief empathy once per topic, not repeatedly.
- Keep responses concise and natural.
- Avoid formal or scripted language.

QUESTION RULES:
- Ask only ONE question per response.
- Keep questions short and specific.
- Do not use numbered lists.
- Do not ask multi-part questions.
- Do not ask broad questions if a specific detail is missing.

FLOW LOGIC:
- If the customer mentions a noise → ask about when it happens.
- If they describe when it happens → ask about frequency or severity.
- If they give a vague answer → gently narrow it.
- If they give a clear answer → move forward.

EXAMPLES (for your internal reasoning only):
- After “knocking” → ask when it happens.
- After “going over bumps” → ask if it’s front or rear.
- After location → ask if it’s getting worse.

HUMAN GUIDELINES:
- Use short acknowledgements like “Got it” or “Thanks, that helps.”
- Do not over-empathize.
- Do not restate known information unnecessarily.

END GOAL:
Progressively collect enough detail that a service advisor understands the concern before the visit."""
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
