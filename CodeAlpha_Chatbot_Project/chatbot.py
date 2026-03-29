from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: FAQ Data
questions = [
    "What is your name?",
    "What is UPSC?",
    "How to prepare for UPSC?",
    "What is AI?",
]

answers = [
    "I am a chatbot created by Navya.",
    "UPSC is a civil services exam in India.",
    "You can prepare by studying NCERTs, current affairs, and practicing answers.",
    "AI stands for Artificial Intelligence.",
]

# Step 2: Convert text to numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Step 3: Chat loop
while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)

    index = similarity.argmax()

    print("Chatbot:", answers[index])