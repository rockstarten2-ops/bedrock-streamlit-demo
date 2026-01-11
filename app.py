import streamlit as st
import boto3
import json

BUSINESS_NAME = "AutoNova Motors"
TAGLINE = "AI Assistant for Sales, Service & Product Intelligence"

st.set_page_config(page_title=BUSINESS_NAME, layout="centered")

st.markdown(f"""
<style>
header {{ visibility: hidden; }}
.title {{
    font-size: 36px;
    font-weight: 700;
}}
.tagline {{
    font-size: 16px;
    color: #555;
    margin-bottom: 20px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='title'>{BUSINESS_NAME}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='tagline'>{TAGLINE}</div>", unsafe_allow_html=True)
st.divider()

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask about vehicles, features, service, or policies...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [
            {"role": "user", "content": f"You are an AI assistant for a premium car manufacturer.\n\n{prompt}"}
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
