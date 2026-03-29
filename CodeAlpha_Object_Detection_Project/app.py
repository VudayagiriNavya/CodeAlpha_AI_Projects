import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO

st.set_page_config(page_title="AI Detection App", layout="wide")

st.title("🚀 Navya's AI Detection System")

# Load model
@st.cache_resource
def load_model():
    return YOLO("yolov8s.pt")

model = load_model()

# Sidebar options
option = st.sidebar.selectbox(
    "Choose Mode",
    ["📸 Image Detection", "🎥 Video Detection", "📷 Camera Detection"]
)

# =========================
# 📸 IMAGE DETECTION
# =========================
if option == "📸 Image Detection":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        results = model(image)
        annotated = results[0].plot()

        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        st.image(annotated, caption="Detected Image")

# =========================
# 🎥 VIDEO DETECTION
# =========================
elif option == "🎥 Video Detection":
    video_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if video_file:
        tfile = open("temp_video.mp4", "wb")
        tfile.write(video_file.read())

        cap = cv2.VideoCapture("temp_video.mp4")

        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)
            annotated = results[0].plot()

            annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

            stframe.image(annotated)

        cap.release()

# =========================
# 📷 CAMERA DETECTION
# =========================
elif option == "📷 Camera Detection":
    run = st.button("Start Camera")

    if run:
        cap = cv2.VideoCapture(0)

        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                st.error("Camera not working")
                break

            results = model(frame)
            annotated = results[0].plot()

            annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

            stframe.image(annotated)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()