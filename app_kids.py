import streamlit as st
import random

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🦁",
    layout="wide"
)

# ---------------------------------
# SESSION STATE
# ---------------------------------
def init_state():
    defaults = {
        "messages": [],
        "stars": 0,
        "asked": set(),
        "event": None,
        "current_answer": None,
        "greeted": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------------------------------
# QUESTION BANK
# ---------------------------------
QUESTIONS = {
    "maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 + 7?", "15"),
    ],
    "science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is the King of the Jungle?", "lion"),
    ],
    "capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
    ]
}

FUN_FACTS = [
    "Lions live in groups called prides 🦁",
    "Mars looks red because of iron dust 🔴",
    "Akola is famous for cotton production 🌱",
]

# ---------------------------------
# EVENT HANDLERS (CRITICAL FIX)
# ---------------------------------
def set_topic(topic):
    st.session_state.event = ("topic", topic)

def set_user_input(text):
    st.session_state.event = ("chat", text)

# ---------------------------------
# SIDEBAR
# ---------------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")

    st.button("➕ Maths", on_click=set_topic, args=("maths",))
    st.button("🔬 Science", on_click=set_topic, args=("science",))
    st.button("🌍 Capitals", on_click=set_topic, args=("capitals",))
    st.button("📖 Stories", on_click=set_topic, args=("stories",))

    st.markdown("---")
    st.caption("Ask anything — even fun facts about Akola 😊")

# ---------------------------------
# LOGIC
# ---------------------------------
def ask_question(topic):
    pool = QUESTIONS.get(topic, [])
    q, a = random.choice(pool)
    st.session_state.current_answer = a.lower()

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🦁 Buddy: Alright Duggu! 😊 {q}"
    })

def handle_answer(text):
    if st.session_state.current_answer is None:
        return False

    if text.lower().strip() == st.session_state.current_answer:
        st.session_state.stars += 1
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🦁 Buddy: 🎉 Awesome Duggu! You got it right! ⭐"
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🦁 Buddy: Nice try Duggu 😊 Let’s keep learning!"
        })

    st.session_state.current_answer = None
    return True

def handle_chat(text):
    text_l = text.lower().strip()

    if text_l in ["hi", "hello", "hey"] and not st.session_state.greeted:
        st.session_state.greeted = True
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Hi Duggu! 😄 I’m so happy you’re here!\n\n"
                "We’ll learn with games, stories, and fun questions.\n"
                "You can click a topic on the left or ask me anything!"
            )
        })
        return

    if handle_answer(text):
        return

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🦁 Buddy: {random.choice(FUN_FACTS)}"
    })

# ---------------------------------
# MAIN UI
# ---------------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.caption("Created with love by your dad ❤️")
st.markdown("---")

for msg in st.session_state.messages:
    st.markdown(msg["content"])

user_input = st.chat_input("Type here 😊")

if user_input:
    set_user_input(user_input)

# ---------------------------------
# EVENT PROCESSOR (SINGLE SOURCE OF TRUTH)
# ---------------------------------
if st.session_state.event:
    kind, value = st.session_state.event
    st.session_state.event = None

    if kind == "topic":
        ask_question(value)

    elif kind == "chat":
        st.session_state.messages.append({
            "role": "user",
            "content": f"🧒 Duggu: {value}"
        })
        handle_chat(value)
