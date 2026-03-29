import streamlit as st
from deep_translator import GoogleTranslator
import pyttsx3
import pyperclip
import speech_recognition as sr

st.set_page_config(page_title="Offline Translation Tool", layout="centered")

# 🎨 Pink Background + Clear Input/Output
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #ff9a9e, #fad0c4);
}
textarea, div.stTextArea>div>textarea {
    background-color: LIGHTBLUE !important;
    color: black !important;
}
div.stButton>button {
    background-color: #ff6f91;
    color: LIGHTBLUE;
}
</style>
""", unsafe_allow_html=True)

st.title("🌐 Translation Tool with Voice Input & TTS")

# 🌍 Languages
languages = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
    "French": "fr", "German": "de", "Spanish": "es", "Italian": "it",
    "Japanese": "ja", "Korean": "ko", "Chinese (Simplified)": "zh-CN",
    "Russian": "ru", "Arabic": "ar", "Portuguese": "pt", "Bengali": "bn",
    "Urdu": "ur", "Malay": "ms", "Vietnamese": "vi", "Dutch": "nl",
    "Greek": "el", "Swedish": "sv", "Polish": "pl"
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From", list(languages.keys()))
with col2:
    target_lang = st.selectbox("To", list(languages.keys()))

# Initialize session_state for input_text
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Input Text Box
st.subheader("Enter Text or Use Voice Input")
st.session_state.input_text = st.text_area("Input Text Here:", value=st.session_state.input_text, height=100)

# 🎤 Offline Voice Input
if st.button("🎤 Speak Now (Offline)"):
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening...")
        r.adjust_for_ambient_noise(source)
        audio_data = r.listen(source)
        try:
            spoken_text = r.recognize_google(audio_data)
            st.session_state.input_text = spoken_text  # Save in session_state
            st.success(f"🎙 You said: {spoken_text}")
        except Exception as e:
            st.error("Could not recognize speech. Try again!")

# Translate
if st.button("Translate"):
    if st.session_state.input_text:
        translated = GoogleTranslator(
            source=languages[source_lang],
            target=languages[target_lang]
        ).translate(st.session_state.input_text)

        st.subheader("✅ Translated Text")
        st.text_area("Output", value=translated, height=150)

        # 📋 Copy Button
        if st.button("📋 Copy Translation"):
            pyperclip.copy(translated)
            st.success("Copied to clipboard!")

        # 🔊 Offline TTS
        engine = pyttsx3.init()
        engine.say(translated)
        engine.runAndWait()
    else:
        st.warning("Please enter or speak text to translate.")