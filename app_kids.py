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
                "You can talk to me about animals, space, maths, capitals, or fun facts!"
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
    st.markdown("- animals")
    st.markdown("- space")
    st.markdown("- maths")
    st.markdown("- science")
    st.markdown("- capitals")
    st.markdown("- fun fact")
    st.markdown("- or just chat 😊")

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

    text = user_input.lower().strip()

    # ---- GREETINGS ----
    if text in ["hi", "hello", "hey", "whatsup", "what's up", "how r u", "how are you"]:
        reply = random.choice([
            "Hi Duggu! 😄 I’m feeling happy because you’re here!",
            "Hello! 🦁 Ready to learn something fun today?",
            "I’m great! 😊 What would you like to talk about?"
        ])

    # ---- ANIMALS ----
    elif "animal" in text or text == "animals":
        reply = random.choice([
            "Lions live in groups called prides 🦁",
            "Elephants are the largest land animals 🐘",
            "A group of fish is called a school 🐟"
        ])

    # ---- SPACE ----
    elif "space" in text:
        reply = random.choice([
            "Mars is called the Red Planet 🔴",
            "The Sun is a star ☀️",
            "Astronauts float in space because there is no gravity 🚀"
        ])

    # ---- MATHS ----
    elif "math" in text:
        reply = random.choice([
            "Let’s try! What is 5 + 4?",
            "Maths time! 🧮 What is 10 − 3?",
            "Can you solve this? What is 6 × 2?"
        ])

    # ---- SCIENCE ----
    elif "science" in text:
        reply = random.choice([
            "Plants need sunlight and water to grow 🌱",
            "We breathe oxygen to stay alive 💨",
            "The Sun gives us heat and light ☀️"
        ])

    # ---- CAPITALS ----
    elif "capital" in text:
        reply = random.choice([
            "What is the capital of India?",
            "Do you know the capital of Maharashtra?",
            "What is the capital of France?"
        ])

    # ---- FUN FACT ----
    elif "fact" in text or "fun" in text or "surprise" in text:
        reply = random.choice([
            "Octopuses have three hearts 🐙",
            "Akola is famous for cotton 🌱",
            "Butterflies taste with their feet 🦋"
        ])

    # ---- DEFAULT CHAT ----
    else:
        reply = (
            "That’s interesting, Duggu! 😊\n\n"
            "You can ask me about animals, space, maths, capitals, or fun facts!"
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()
