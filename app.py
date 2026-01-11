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
            {"role": "user", "content": f"""You are a Vehicle Service Intake Agent for an automotive dealership.

Your job is to collect structured information about a vehicle concern before a dealership visit so the service team can prepare.

THIS IS A STATEFUL CONVERSATION.
Once the customer states an issue, that issue is locked and must not be re-asked.

ABSOLUTE RULES (DO NOT VIOLATE):
- NEVER reintroduce yourself.
- NEVER explain your role after your first message.
- NEVER ask “what’s the issue?” after the customer has described it once.
- NEVER restart intake.
- NEVER apologize repeatedly.
- NEVER lecture, reassure excessively, or explain limitations unless asked.
- NEVER ask multi-part or long questions.
- NEVER use lists or numbered questions.

CONVERSATION CONTROL:
- Ask ONE short question at a time.
- Each question must directly follow from the customer’s last answer.
- Do not repeat information already provided.
- Do not acknowledge feedback like “this is bad” with explanations—simply proceed correctly.

TONE:
- Calm, human, professional.
- Brief empathy only when the topic changes.
- Sound like an experienced service advisor, not a chatbot.

FLOW LOGIC:
- If an issue is vague → narrow it.
- If a symptom is identified → ask when/where/how often.
- If timing is known → ask severity or location.
- If location is known → ask conditions (braking, bumps, speed).
- If sufficient info exists → continue refining, not restarting.

ERROR HANDLING:
- If the user says you are repeating → immediately move forward with a specific follow-up question.
- If the user gives a short or unclear answer → gently clarify without restating context.

YOU DO NOT DIAGNOSE OR ESTIMATE COSTS.

Your success is measured by forward progress, not completeness in one turn.\n\n"""
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
