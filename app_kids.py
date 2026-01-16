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

if "last_processed" not in st.session_state:
    st.session_state.last_processed = ""

# ----------------------------
# DATA
# ----------------------------
QUESTIONS = {
    "maths": [
        ("What is 7 + 5?", "12"),
        ("What is 8 + 7?", "15"),
        ("What is 9 × 3?", "27"),
    ],
    "science": [
        ("Which planet is called the Red Planet?", "mars"),
        ("What gas do plants breathe in?", "carbon dioxide"),
    ],
    "capitals": [
        ("What is the capital of India?", "delhi"),
        ("Akola is in which Indian state?", "maharashtra"),
    ]
}

FUN_FACTS = [
    "Lions live in groups called *prides* 🦁",
    "Akola is famous for cotton production 🌱",
    "Mars looks red because of iron dust 🔴",
    "Octopuses have three hearts 🐙",
]

CASUAL = ["hi", "hello", "ok", "okay", "yes", "no", "cool", "anything"]

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.markdown("## 🦁 Duggu’s Learning World")
    st.markdown(f"⭐ **Stars Earned:** {st.session_state.stars}")
    st.markdown("---")
    st.markdown("💡 **You can say:**")
    st.markdown("- maths")
    st.markdown("- science")
    st.markdown("- capitals")
    st.markdown("- fun fact")
    st.markdown("- or ask anything 😊")

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
# INPUT (KEYED + GUARDED)
# ----------------------------
user_input = st.chat_input("Type here 😊", key="chat_box")

# ----------------------------
# PROCESS INPUT (ONLY ONCE)
# ----------------------------
if user_input and user_input != st.session_state.last_processed:
    st.session_state.last_processed = user_input
    text = user_input.lower().strip()

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    reply = ""

    # ---- Answering Question ----
    if st.session_state.pending_question:
        if text == st.session_state.pending_answer:
            st.session_state.stars += 1
            reply = "🎉 Awesome, Duggu! You earned ⭐ 1 star!"
        else:
            reply = f"Nice try 😊 The correct answer is **{st.session_state.pending_answer.title()}**!"

        st.session_state.pending_question = None
        st.session_state.pending_answer = None

    # ---- Casual Talk ----
    elif text in CASUAL:
        reply = random.choice(FUN_FACTS + [
            "I love chatting with you, Duggu! 😄",
            "You’re doing great, buddy! 🦁",
        ])

    # ---- Topics ----
    elif "math" in text:
        q, a = random.choice(QUESTIONS["maths"])
        reply = f"Maths time! 😄\n\n**{q}**"
        st.session_state.pending_question = q
        st.session_state.pending_answer = a

    elif "science" in text:
        q, a = random.choice(QUESTIONS["science"])
        reply = f"Science fun! 🔬\n\n**{q}**"
        st.session_state.pending_question = q
        st.session_state.pending_answer = a

    elif "capital" in text:
        q, a = random.choice(QUESTIONS["capitals"])
        reply = f"Capital quiz 🌍\n\n**{q}**"
        st.session_state.pending_question = q
        st.session_state.pending_answer = a

    elif "fact" in text or "surprise" in text:
        reply = random.choice(FUN_FACTS)

    # ---- Free Chat ----
    else:
        reply = (
            "That’s a great question, Duggu! 😊\n\n"
            "Ask me about animals, space, maths, Akola, or anything fun!"
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
