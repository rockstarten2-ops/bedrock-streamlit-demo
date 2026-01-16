import streamlit as st
import random

# ----------------------------------
# PAGE SETUP
# ----------------------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🦁",
    layout="wide"
)

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "pending_answer" not in st.session_state:
    st.session_state.pending_answer = None

# ----------------------------------
# QUESTION BANK (STARTERS, NOT LIMITS)
# ----------------------------------
QUESTIONS = {
    "maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 + 7?", "15"),
        ("What is 12 × 2?", "24"),
    ],
    "science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is known as the King of the Jungle?", "lion"),
    ],
    "capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
    ],
}

FUN_FACTS = [
    "Lions live in groups called prides 🦁",
    "Mars looks red because of iron dust 🔴",
    "Akola is famous for cotton production 🌱",
]

PRAISE = [
    "Awesome job, Duggu! 🎉",
    "High five! ✋",
    "You’re learning fast! 🚀",
    "Great thinking, buddy! 😄",
]

# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.markdown("Created with love by your dad ❤️")
st.markdown("---")

# ----------------------------------
# CHAT DISPLAY
# ----------------------------------
for msg in st.session_state.messages:
    st.markdown(f"**{msg['role']}:** {msg['content']}")

# ----------------------------------
# CHAT INPUT (ONLY INPUT MECHANISM)
# ----------------------------------
user_input = st.chat_input("Type here 😊")

if user_input:
    user_text = user_input.lower().strip()

    # Show user message
    st.session_state.messages.append({
        "role": "🧒 Duggu",
        "content": user_input
    })

    # ----------------------------------
    # CHECK ANSWER IF A QUESTION IS PENDING
    # ----------------------------------
    if st.session_state.pending_question:
        correct = st.session_state.pending_answer

        if correct in user_text:
            st.session_state.stars += 1
            reply = f"{random.choice(PRAISE)} ⭐ You earned 1 star!"
        else:
            reply = f"Nice try, Duggu 😊 The correct answer is **{correct.title()}**."

        st.session_state.pending_question = None
        st.session_state.pending_answer = None

    # ----------------------------------
    # TOPIC OR FREE CHAT
    # ----------------------------------
    else:
        if "math" in user_text:
            q, a = random.choice(QUESTIONS["maths"])
            reply = f"Let’s do some maths, Duggu! 😄\n\n**{q}**"
            st.session_state.pending_question = q
            st.session_state.pending_answer = a

        elif "science" in user_text:
            q, a = random.choice(QUESTIONS["science"])
            reply = f"Science time! 🔬\n\n**{q}**"
            st.session_state.pending_question = q
            st.session_state.pending_answer = a

        elif "capital" in user_text:
            q, a = random.choice(QUESTIONS["capitals"])
            reply = f"Let’s test capitals 🌍\n\n**{q}**"
            st.session_state.pending_question = q
            st.session_state.pending_answer = a

        elif "fact" in user_text or "surprise" in user_text:
            reply = random.choice(FUN_FACTS)

        else:
            reply = (
                "I love your curiosity, Duggu! 🦁\n\n"
                "You can say **maths**, **science**, **capitals**, or ask me anything fun!"
            )

    # Show buddy response
    st.session_state.messages.append({
        "role": "🦁 Buddy",
        "content": reply
    })

    st.rerun()

# ----------------------------------
# SIDEBAR (INFO ONLY, NO INTERACTION)
# ----------------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")
    st.markdown("💡 You can ask:")
    st.markdown("- Maths")
    st.markdown("- Science")
    st.markdown("- Capitals")
    st.markdown("- Fun facts")
