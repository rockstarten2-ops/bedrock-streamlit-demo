import streamlit as st
import random

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🦁",
    layout="wide"
)

# --------------------
# SESSION STATE
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi Duggu! 👋🦁\n\n"
                "I’m Buddy, your learning friend 😊\n\n"
                "You can talk to me about *anything* — "
                "school, animals, space, stories, or just chat!"
            )
        }
    ]

# --------------------
# SIDEBAR
# --------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown("⭐ Stars Earned: 0")
    st.markdown("---")
    st.markdown("💬 You can:")
    st.markdown("- Ask questions")
    st.markdown("- Share ideas")
    st.markdown("- Learn fun things")
    st.markdown("- Just chat 😊")

# --------------------
# CHAT HISTORY
# --------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧒 **Duggu:** {msg['content']}")
    else:
        st.markdown(f"🦁 **Buddy:** {msg['content']}")

# --------------------
# INPUT (ENTER ONLY)
# --------------------
user_input = st.chat_input("Type here 😊")

if user_input:
    # 1️⃣ Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    text = user_input.strip().lower()

    # 2️⃣ Response logic
    greetings = [
        "Hey Duggu! 😄",
        "Hello there! 🦁",
        "Hi! I’m happy you’re here 😊"
    ]

    encouragements = [
        "That’s interesting, Duggu! 😊",
        "I like how you think! 🧠",
        "Nice thought! 😄",
        "I’m glad you shared that 🦁"
    ]

    fun_facts = [
        "Did you know? Octopuses have three hearts 🐙",
        "Mars looks red because of iron dust 🔴",
        "The Moon has no air 🌙",
        "Tigers have striped skin too 🐯",
        "Akola is famous for cotton 🌱"
    ]

    if text in ["hi", "hello", "hey", "whatsup", "what's up"]:
        reply = random.choice(greetings)

    elif "?" in text:
        reply = (
            f"{random.choice(encouragements)}\n\n"
            "Let me explain it simply 😊"
        )

    else:
        reply = (
            f"{random.choice(encouragements)}\n\n"
            f"{random.choice(fun_facts)}"
        )

    # 3️⃣ Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # 4️⃣ CRITICAL: STOP EXECUTION
    st.stop()
