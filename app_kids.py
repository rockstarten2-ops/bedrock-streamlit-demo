import streamlit as st
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Duggu’s Learning World",
    page_icon="🧸",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()

if "current_topic" not in st.session_state:
    st.session_state.current_topic = None

# -----------------------------
# QUESTION BANK (STARTER)
# -----------------------------
QUESTIONS = {
    "Maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 + 7?", "15"),
        ("What is 12 × 2?", "24"),
    ],
    "Science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("Which animal is known as the King of the Jungle?", "lion"),
    ],
    "Capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
        ("What is the capital of Thailand?", "bangkok"),
    ],
    "Games": [
        ("I’m thinking of a number between 1 and 10. Is it 5?", None),
    ],
    "Stories": [
        ("Do you want to hear a brave story about Prithviraj Chauhan?", None),
    ]
}

# -----------------------------
# HELPERS
# -----------------------------
def buddy_say(text):
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"🧸 **Buddy:** {text}"
    })

def duggu_say(text):
    st.session_state.messages.append({
        "role": "user",
        "content": f"🧒 **Duggu:** {text}"
    })

def ask_new_question(topic):
    available = [
        q for q in QUESTIONS.get(topic, [])
        if q[0] not in st.session_state.asked_questions
    ]

    if not available:
        buddy_say("Awesome learning, Duggu! 🎉 Want to try something else or ask me anything?")
        return

    question, answer = random.choice(available)
    st.session_state.asked_questions.add(question)

    buddy_say(f"Hey Duggu 😊 {question}")
    st.session_state.current_answer = answer

def handle_answer(user_text):
    answer = st.session_state.get("current_answer")

    if answer is None:
        buddy_say("That’s interesting, Duggu! 😄 Tell me more or ask me anything.")
        return

    if user_text.strip().lower() == answer:
        st.session_state.stars += 1
        buddy_say(f"🎉 Great job, Duggu! You earned ⭐ 1 star!")
    else:
        buddy_say("Nice try, Duggu 💪 Learning is about trying!")

    st.session_state.current_answer = None

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🧸 Duggu’s Learning World")

    st.markdown("### 🌟 Stars Earned")
    st.markdown(f"**⭐ {st.session_state.stars}**")

    st.markdown("---")
    st.markdown("### 🎯 Explore")

    def topic_link(label, topic):
        if st.button(label, use_container_width=True):
            st.session_state.current_topic = topic
            buddy_say(f"Yay Duggu! Let’s explore **{topic}** together 🚀")
            ask_new_question(topic)

    topic_link("➕ Maths", "Maths")
    topic_link("🔬 Science", "Science")
    topic_link("🌍 Capitals", "Capitals")
    topic_link("🎮 Games", "Games")
    topic_link("📖 Stories", "Stories")

    st.markdown("---")
    st.markdown("💡 *Ask me anything — even fun facts about Akola!* 😄")

# -----------------------------
# MAIN HEADER
# -----------------------------
st.markdown("## Hi Duggu! 👋")
st.markdown("### I’m your learning buddy 😊")
st.markdown("We’ll learn with games, stories, and fun questions!")
st.markdown("_Created with love by your dad ❤️_")

st.markdown("---")

# -----------------------------
# CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# USER INPUT (FREE CHAT)
# -----------------------------
user_input = st.chat_input("Ask me anything 😊")

if user_input:
    duggu_say(user_input)

    if st.session_state.get("current_answer") is not None:
        handle_answer(user_input)
    else:
        # Free chat (age-safe)
        buddy_say(
            "That’s a great question, Duggu! 🤗 "
            "I love how curious you are. "
            "Want a fun question or a story next?"
        )
