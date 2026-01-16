import streamlit as st
import random

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🦁",
    layout="wide"
)

# --------------------------------
# SESSION STATE
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()

if "greeted" not in st.session_state:
    st.session_state.greeted = False

# --------------------------------
# QUESTION BANK (starter pool)
# --------------------------------
QUESTIONS = [
    ("What is 7 + 5?", "12"),
    ("Which planet is called the Red Planet?", "mars"),
    ("Which animal is the King of the Jungle?", "lion"),
    ("What is the capital of India?", "delhi"),
    ("Akola is in which Indian state?", "maharashtra"),
]

FUN_FACTS = [
    "Did you know? Akola is famous for cotton production! 🌱",
    "Lions live in groups called prides 🦁",
    "Mars looks red because of iron dust 🔴",
]

# --------------------------------
# SIDEBAR
# --------------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")

    if st.button("➕ Maths"):
        ask_random_question()

    if st.button("🔬 Science"):
        ask_random_question()

    if st.button("🌍 Capitals"):
        ask_random_question()

    if st.button("📖 Stories"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🦁 Buddy: Once upon a time, there was a brave king named Prithviraj Chauhan who loved his land and people. Want to hear more? 😊"
        })

    st.markdown("---")
    st.caption("Ask anything — even fun facts about Akola 😊")

# --------------------------------
# FUNCTIONS
# --------------------------------
def ask_random_question():
    available = [q for q in QUESTIONS if q[0] not in st.session_state.asked_questions]
    if not available:
        st.session_state.asked_questions.clear()
        available = QUESTIONS

    q, a = random.choice(available)
    st.session_state.asked_questions.add(q)
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🦁 Buddy: Alright Duggu! 😊 {q}"
    })
    st.session_state.current_answer = a.lower()


def handle_answer(user_text):
    if "current_answer" not in st.session_state:
        return False

    if user_text.lower().strip() == st.session_state.current_answer:
        st.session_state.stars += 1
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🦁 Buddy: 🎉 Awesome Duggu! You got it right! ⭐"
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🦁 Buddy: Nice try Duggu! 😊 Learning is about trying!"
        })

    del st.session_state.current_answer
    ask_random_question()
    return True


def handle_free_chat(text):
    text = text.lower().strip()

    if text in ["hi", "hello", "hey"] and not st.session_state.greeted:
        st.session_state.greeted = True
        return (
            "Hi Duggu! 😄 I’m so happy you’re here!\n\n"
            "Let’s learn with games, stories, and fun questions!\n"
            "You can also say *surprise* 😉"
        )

    if text in ["anything", "surprise"]:
        ask_random_question()
        return None

    # fallback fun response
    return random.choice(FUN_FACTS)

# --------------------------------
# MAIN UI
# --------------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.caption("Created with love by your dad ❤️")
st.markdown("---")

# --------------------------------
# CHAT HISTORY
# --------------------------------
for msg in st.session_state.messages:
    st.markdown(msg["content"])

# --------------------------------
# USER INPUT
# --------------------------------
user_input = st.chat_input("Type here 😊")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": f"🧒 Duggu: {user_input}"
    })

    if not handle_answer(user_input):
        reply = handle_free_chat(user_input)
        if reply:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"🦁 Buddy: {reply}"
            })
