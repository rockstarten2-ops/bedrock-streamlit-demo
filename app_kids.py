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
# SESSION STATE INIT
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi Duggu! 👋🦁\n\n"
                "I’m Buddy, your learning friend 😊\n\n"
                "You can talk to me about *anything* — "
                "school, animals, space, stories, or just what you’re thinking!"
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
# USER INPUT (ENTER ONLY)
# --------------------
user_input = st.chat_input("Type here 😊")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    text = user_input.strip().lower()

    # --------------------
    # FRIENDLY RESPONSE LOGIC
    # --------------------
    acknowledgements = [
        "That’s interesting, Duggu! 😊",
        "I like how you’re thinking! 🧠",
        "That’s a good thought! 😄",
        "I’m glad you told me that! 🦁"
    ]

    greetings = [
        "Hi Duggu! 😄 I’m happy you’re here!",
        "Hello! 🦁 What’s on your mind today?",
        "Hey there! 😊 Ready to chat?"
    ]

    followups = [
        "Want to hear something cool?",
        "Should I tell you a fun fact?",
        "What made you think about that?",
        "Do you want to learn something new?"
    ]

    fun_facts = [
        "Did you know? Octopuses have three hearts 🐙",
        "Fun fact! Mars looks red because of iron dust 🔴",
        "Cool one! Tigers have striped skin, not just fur 🐯",
        "Guess what? The Moon has no air 🌙",
        "Did you know? Akola is famous for cotton production 🌱"
    ]

    # --------------------
    # RESPONSE DECISION
    # --------------------
    if text in ["hi", "hello", "hey", "whatsup", "what's up"]:
        reply = random.choice(greetings)

    elif text in ["ok", "okay", "yes", "yeah", "yep", "hmm"]:
        reply = random.choice(followups)

    elif "?" in text or text.startswith(("what", "why", "how", "when", "where")):
        reply = (
            f"{random.choice(acknowledgements)}\n\n"
            "Let me explain it in a simple way 😊"
        )

    else:
        reply = (
            f"{random.choice(acknowledgements)}\n\n"
            f"{random.choice(fun_facts)}"
        )

    # Add assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
