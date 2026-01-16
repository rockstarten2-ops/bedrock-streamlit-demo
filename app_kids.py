import streamlit as st
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🦁",
    layout="wide"
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "last_question" not in st.session_state:
    st.session_state.last_question = None

# -----------------------------
# QUESTION BANK (starter only)
# These are NOT fixed – app can also chat freely
# -----------------------------
QUESTION_BANK = {
    "Maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 + 7?", "15"),
        ("What is 6 × 4?", "24"),
    ],
    "Science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is known as the King of the Jungle?", "lion"),
    ],
    "Capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
    ],
    "Stories": [
        ("Do you want to hear a brave story about Prithviraj Chauhan?", None)
    ]
}

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")

    st.markdown("### Explore")
    if st.button("➕ Maths"):
        st.session_state.last_question = ask_topic_question("Maths")

    if st.button("🔬 Science"):
        st.session_state.last_question = ask_topic_question("Science")

    if st.button("🌍 Capitals"):
        st.session_state.last_question = ask_topic_question("Capitals")

    if st.button("📖 Stories"):
        st.session_state.last_question = ask_topic_question("Stories")

    st.markdown("---")
    st.caption("Ask anything — even fun facts about Akola 😊")

# -----------------------------
# FUNCTIONS
# -----------------------------
def ask_topic_question(topic):
    q, a = random.choice(QUESTION_BANK[topic])
    st.session_state.messages.append(
        {"role": "assistant", "content": f"🦁 Buddy: {q}"}
    )
    return {"question": q, "answer": a}


def handle_free_chat(user_text):
    greetings = ["hi", "hello", "hey"]
    if user_text.lower().strip() in greetings:
        return (
            "Hi Duggu! 😄 I’m so happy you’re here!\n\n"
            "You can:\n"
            "➕ Play with Maths\n"
            "🔬 Explore Science\n"
            "🌍 Learn Capitals\n"
            "📖 Hear fun stories\n\n"
            "Or just ask me anything!"
        )
    return None


def check_answer(user_text):
    q = st.session_state.last_question
    if not q or not q["answer"]:
        return False

    if user_text.lower().strip() == q["answer"]:
        st.session_state.stars += 1
        st.session_state.last_question = None
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"🦁 Buddy: 🎉 Great job Duggu! You earned ⭐ 1 star!"
            }
        )
        return True

    return False


# -----------------------------
# MAIN UI
# -----------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.caption("We’ll learn with games, stories, and fun questions!")
st.caption("Created with love by your dad ❤️")
st.markdown("---")

# -----------------------------
# CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Type here 😊")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": f"🧒 Duggu: {user_input}"}
    )

    # 1️⃣ Check free chat first (prevents hanging)
    free_reply = handle_free_chat(user_input)
    if free_reply:
        st.session_state.messages.append(
            {"role": "assistant", "content": f"🦁 Buddy: {free_reply}"}
        )

    # 2️⃣ Check answer if a question exists
    elif check_answer(user_input):
        pass

    # 3️⃣ Otherwise respond naturally
    else:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "🦁 Buddy: Nice thinking, Duggu! 😊\n\n"
                    "Want to try a question from Maths, Science, Capitals, or hear a fun story?"
                )
            }
        )
