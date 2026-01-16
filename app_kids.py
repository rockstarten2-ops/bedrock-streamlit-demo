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
                "I’m your learning buddy 😊\n\n"
                "You can ask me about maths, science, capitals, animals, or fun facts!"
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
    st.markdown("💡 You can say:")
    st.markdown("- maths")
    st.markdown("- science")
    st.markdown("- capitals")
    st.markdown("- fun fact")
    st.markdown("- or ask anything 😊")

# --------------------
# CHAT DISPLAY
# --------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧒 **Duggu:** {msg['content']}")
    else:
        st.markdown(f"🦁 **Buddy:** {msg['content']}")

# --------------------
# USER INPUT (ENTER WORKS)
# --------------------
user_input = st.chat_input("Type here 😊")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    text = user_input.lower()

    if "math" in text:
        reply = random.choice([
            "Let’s do maths! 😊 What is 5 + 3?",
            "Maths time! 🧮 What is 10 − 4?",
            "Try this: What is 6 × 2?"
        ])

    elif "science" in text:
        reply = random.choice([
            "Science is fun! 🔬 Which planet is called the Red Planet?",
            "What gas do plants breathe in?",
            "Why do we need the Sun?"
        ])

    elif "capital" in text:
        reply = random.choice([
            "What is the capital of India?",
            "Do you know the capital of Maharashtra?",
            "What is the capital of France?"
        ])

    elif "fact" in text or "surprise" in text:
        reply = random.choice([
            "Lions live in groups called prides 🦁",
            "Octopuses have three hearts 🐙",
            "Mars looks red because of iron dust 🔴",
            "Akola is famous for cotton 🌱"
        ])

    else:
        reply = (
            "That’s interesting, Duggu! 😊\n\n"
            "You can ask me about maths, science, capitals, animals, or fun facts!"
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()
