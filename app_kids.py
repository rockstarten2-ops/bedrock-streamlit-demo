import streamlit as st
import random

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Duggu's Learning World",
    page_icon="🦁",
    layout="wide"
)

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "pending_answer" not in st.session_state:
    st.session_state.pending_answer = None

# ----------------------------
# QUESTION BANKS
# ----------------------------
QUESTIONS = {
    "maths": [
        ("What is 7 + 5?", "12"),
        ("What is 9 × 3?", "27"),
        ("What is 15 − 6?", "9"),
        ("What is 8 + 7?", "15"),
    ],
    "science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("What gas do plants breathe in?", "carbon dioxide"),
        ("Which part of the plant makes food?", "leaf"),
    ],
    "capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
        ("What is the capital of Maharashtra?", "mumbai"),
    ]
}

FUN_FACTS = [
    "Did you know? Lions live in groups called *prides* 🦁",
    "Akola is famous for cotton production 🌱",
    "Mars looks red because of iron dust 🔴",
    "Octopuses have three hearts 🐙",
    "The Moon has no air 🌕",
]

CASUAL_WORDS = ["ok", "okay", "yes", "anything", "hmm", "cool", "hi", "hello"]

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")
    st.markdown("💡 **You can say:**")
    st.markdown("- Maths")
    st.markdown("- Science")
    st.markdown("- Capitals")
    st.markdown("- Surprise / Fun fact")
    st.markdown("- Or ask *anything!* 😊")

# ----------------------------
# HEADER
# ----------------------------
st.markdown(
    """
    <div style="text-align:center;">
        <h1>Hi Duggu! 👋</h1>
        <h3>I’m your learning buddy 😊</h3>
        <p>We’ll learn with games, stories, and fun questions!</p>
        <p><i>Created with love by your dad ❤️</i></p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# CHAT DISPLAY
# ----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧒 **Duggu:** {msg['content']}")
    else:
        st.markdown(f"🦁 **Buddy:** {msg['content']}")

# ----------------------------
# INPUT
# ----------------------------
user_input = st.chat_input("Type here 😊")

# ----------------------------
# LOGIC
# ----------------------------
if user_input:
    user_text = user_input.strip().lower()

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    reply = ""

    # ---- ANSWERING A QUESTION ----
    if st.session_state.pending_question:
        if user_text == st.session_state.pending_answer:
            st.session_state.stars += 1
            reply = f"🎉 Great job, Duggu! You earned ⭐ 1 star!"
        else:
            reply = f"Nice try, Duggu 😊 The correct answer is **{st.session_state.pending_answer.title()}**!"

        st.session_state.pending_question = None
        st.session_state.pending_answer = None

    # ---- CASUAL CHAT ----
    elif user_text in CASUAL_WORDS:
        reply = random.choice(FUN_FACTS + [
            "You're doing great, Duggu! 😄",
            "I love chatting with you 🦁",
        ])

    # ---- TOPICS ----
    elif "math" in user_text:
        q, a = random.choice(QUESTIONS["maths"])
        reply = f"Let’s play with maths, Duggu! 😄\n\n**{q}**"
        st.session_state.pending_question = q
        st.session_state.pending_answer = a

    elif "science" in user_text:
        q, a = random.choice(QUESTIONS["science"])
        reply = f"Science time! 🔬\n\n**{q}**"
        st.session_state.pending_question = q
        st.session_state.pending_answer = a

    elif "capital" in user_text:
        q, a = random.choice(QUESTIONS["capitals"])
        reply = f"Let’s learn capitals 🌍\n\n**{q}**"
        st.session_state.pending_question = q
        st.session_state.pending_answer = a

    elif "fact" in user_text or "surprise" in user_text:
        reply = random.choice(FUN_FACTS)

    # ---- FREE QUESTION MODE ----
    else:
        reply = (
            "That’s a great question, Duggu! 😊\n\n"
            "I can help with school topics or fun facts. "
            "Try asking about animals, space, maths, or Akola!"
        )

    # Add buddy reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
