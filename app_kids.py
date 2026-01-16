import streamlit as st
import boto3
import json

# ===============================
# Page config
# ===============================
st.set_page_config(
    page_title="Hi Duggu!",
    page_icon="🤖",
    layout="centered"
)

# ===============================
# Header with Mascot
# ===============================
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:15px;">
        <div style="font-size:60px;">🤖</div>
        <div>
            <h2 style="margin-bottom:0;">Hi Duggu! 👋</h2>
            <p style="margin-top:4px; font-size:18px;">
                I’m your learning buddy 😊
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "Ask me a question or choose a topic below. "
    "We’ll figure it out together!"
)

st.divider()

# ===============================
# Initialize session state
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi Duggu! What would you like to learn today? 📚"
        }
    ]

# ===============================
# Topic buttons (Kid-friendly)
# ===============================
st.markdown("### Choose a topic 👇")

col1, col2, col3, col4 = st.columns(4)

topic = None

with col1:
    if st.button("➕ Maths"):
        topic = "Maths"

with col2:
    if st.button("🔬 Science"):
        topic = "Science"

with col3:
    if st.button("📖 English"):
        topic = "English"

with col4:
    if st.button("🌍 GK"):
        topic = "General Knowledge"

if topic:
    st.session_state.messages.append({
        "role": "user",
        "content": f"I want to learn {topic}"
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Awesome choice, Duggu! 😄 Let’s learn {topic}. What would you like to start with?"
    })

# ===============================
# Display chat history
# ===============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# Chat input (fixed at bottom)
# ===============================
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # ===============================
    # Claude Sonnet (UNCHANGED)
    # ===============================
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    system_prompt = (
        "You are a friendly, patient learning buddy for a Grade 4 student named Duggu. "
        "Explain concepts very simply, use examples, emojis when helpful, "
        "and encourage curiosity. Never use advanced language."
    )

    conversation = [
        {"role": "system", "content": system_prompt}
    ]

    for m in st.session_state.messages:
        conversation.append({
            "role": m["role"],
            "content": m["content"]
        })

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "messages": conversation,
            "max_tokens": 500,
            "temperature": 0.5
        })
    )

    result = json.loads(response["body"].read())
    assistant_reply = result["content"][0]["text"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

# ===============================
# Footer (Dad's note ❤️)
# ===============================
st.divider()
st.markdown(
    """
    <div style="text-align:center; font-size:14px; color:gray;">
        ❤️ Created with love by your Dad ❤️
    </div>
    """,
    unsafe_allow_html=True
)
