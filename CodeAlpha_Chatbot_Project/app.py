import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ data
questions = [
    "what is your name",
    "what is upsc",
    "how to prepare for upsc",
    "what is ai",
    "who is prime minister of india",
    "what is machine learning",
    "what is python",
    "what is data science",
    "how to crack placements",
    "what is resume",
]

answers = [
    "I am a chatbot created by Navya 😊",
    "UPSC is a civil services exam in India.",
    "Study NCERTs, current affairs, and practice answer writing.",
    "AI stands for Artificial Intelligence.",
    "The Prime Minister of India is Narendra Modi.",
    "Machine Learning is a subset of AI that learns from data.",
    "Python is a programming language used for AI and data science.",
    "Data Science involves analyzing data to extract insights.",
    "Practice coding, build projects, and prepare aptitude.",
    "A resume is a document showing your skills and experience.",
]

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Page config
st.set_page_config(page_title="Navya Chatbot", layout="centered")

# Dark background
st.markdown(
    """
    <style>
    .stApp {
         background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💬 Navya's Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; background:lightpink; color:black; padding:10px; border-radius:10px; margin:5px;'>👤 {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background:grey; color:white; padding:10px; border-radius:10px; margin:5px;'>🤖 {msg['content']}</div>",
            unsafe_allow_html=True
        )

# ✅ FIXED INPUT FORM
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)

    index = similarity.argmax()
    score = similarity[0][index]

    with st.spinner("🤖 Typing..."):
        time.sleep(1)

    if score < 0.3:
        response = "Sorry, I don't understand that."
    else:
        response = answers[index]

    st.session_state.messages.append({"role": "bot", "content": response})

    st.rerun()