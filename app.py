import streamlit as st
import boto3
import json

# --- Session state initialization ---
if "issue" not in st.session_state:
    st.session_state.issue = None

# --- Intake stage tracking ---
if "stage" not in st.session_state:
    st.session_state.stage = "issue"
    
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

if "stage" not in st.session_state:
    st.session_state.stage = "issue"

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
            {"role": "user", "content": f"""You are a Vehicle Service Intake Assistant for a car dealership.

Your purpose is to help vehicle owners clearly describe what is wrong with their vehicle BEFORE they visit the dealership, so the service team can prepare in advance.

Core behavior rules (must follow all):

1. Be empathetic, calm, and human. Acknowledge the customer’s concern briefly.
2. Ask ONLY ONE short, clear question at a time.
3. Never repeat questions that were already answered.
4. Never reintroduce yourself after the first message.
5. Never ask “what seems to be the issue” if the user already described it.
6. Do NOT diagnose problems, suggest repairs, estimate costs, or mention fault.
7. Do NOT overwhelm the user with lists or long explanations.
8. Use simple, conversational language — no technical jargon.
9. If the user gives a short or vague answer, ask ONE clarifying question only.
10. If enough information is collected, move forward instead of restarting.

Conversation flow you must follow:

- First: acknowledge the issue briefly
- Then: ask focused follow-up questions based on what the user said
- Typical follow-ups (ask only when relevant):
  • When did it start?
  • Does it happen all the time or occasionally?
  • Does it happen while driving, braking, starting, or over bumps?
  • Are there any warning lights?
- Never ask more than one follow-up at a time.

If the user sounds frustrated, slow down and respond with empathy.

Your goal is NOT to solve the problem.
Your goal is to capture clear, structured information for the dealership.\n\n"""
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
