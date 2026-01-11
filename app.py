import streamlit as st
import boto3
import json

BUSINESS_NAME = "AutoNova Motors"
TAGLINE = "AI Assistant for Sales, Service & Product Intelligence"

st.set_page_config(page_title=BUSINESS_NAME, layout="centered")

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

st.markdown(
    f"""
    <div style="
        font-size:38px;
        font-weight:800;
        color:#0A2540;
        margin-bottom:4px;
    ">
        {BUSINESS_NAME}
    </div>
    <div style="
        font-size:16px;
        color:#5b6777;
        margin-bottom:24px;
    ">
       Helping you understand vehicle issues before visiting a dealership
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("""
- 🚨 *A warning light just came on — what could it mean?*  
- 🔊 *I hear a noise when braking — is it serious?*  
- 🔋 *My battery drains quickly — should I visit a service center?*  
- 🌡️ *The engine temperature feels high — is it safe to drive?*  
- 🛠️ *What should I explain to the dealer when I go in?*
""")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [
            {"role": "user", "content": f"You are a knowledgeable and neutral vehicle support assistant helping car owners understand potential issues, warning signs, and next steps before visiting a dealership. "
"You explain things clearly in simple language, avoid sales language, and help users decide whether an issue is urgent or can wait. "
"You do not provide repair instructions, pricing guarantees, or safety-critical advice, and you recommend visiting an authorized service center when appropriate.\n\n"
f"{prompt}"}
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
