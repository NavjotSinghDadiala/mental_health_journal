import random
import tkinter as tk
import webbrowser

# ----------------------------- Emotion Content -----------------------------
emotion_data = {
    "sad": {
        "videos": [
            "https://youtu.be/ZXsQAXx_ao0",
            "https://youtu.be/VbfpW0pbvaU",
            "https://youtu.be/wnHW6o8WMas"
        ],
        "quotes": ["Tough times never last, but tough people do."],
        "affirmations": ["I am stronger than my sadness."]
    },
    "angry": {
        "videos": [
            "https://youtu.be/fLJsdqxnZb0",
            "https://youtu.be/fHO_qxG1L0Y",
            "https://youtu.be/LWbOOGGQ6LQ"
        ],
        "quotes": ["Anger is one letter short of danger."],
        "affirmations": ["I am in control of my emotions."]
    },
    "happy": {
        "videos": [
            "https://youtu.be/d-diB65scQU",
            "https://youtu.be/HgzGwKwLmgM",
            "https://youtu.be/3GwjfUFyY6M"
        ],
        "quotes": ["Happiness is a journey, not a destination."],
        "affirmations": ["I radiate joy and kindness."]
    },
    "anxious": {
        "videos": [
            "https://youtu.be/1z3O_z0qT3I",
            "https://youtu.be/WWloIAQpMcQ",
            "https://youtu.be/T5kGRa7l3A0"
        ],
        "quotes": ["Breathe. You are strong enough to handle this."],
        "affirmations": ["I am grounded, calm, and in control."]
    }
}

# ----------------------------- Emotion Detection -----------------------------
def detect_emotion(text):
    text = text.lower()
    # Calculate confidence based on keyword matches
    confidence = 0.0
    emotion = "happy"  # default
    
    # Define emotion keywords and their weights
    emotion_keywords = {
        "sad": ["sad", "cry", "down", "depressed", "unhappy", "miserable"],
        "angry": ["angry", "mad", "furious", "rage", "annoyed", "irritated"],
        "happy": ["happy", "joy", "grateful", "excited", "good", "great"],
        "anxious": ["anxious", "worried", "nervous", "panic", "stressed", "tense"]
    }
    
    # Count matches for each emotion
    matches = {emotion: 0 for emotion in emotion_keywords}
    for word in text.split():
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in word for keyword in keywords):
                matches[emotion] += 1
    
    # Find the emotion with most matches
    max_matches = max(matches.values())
    if max_matches > 0:
        emotion = max(matches, key=matches.get)
        # Calculate confidence (0.5 to 1.0)
        confidence = 0.5 + (0.5 * (max_matches / len(text.split())))
    else:
        # If no matches, return default with low confidence
        confidence = 0.3
    
    return emotion, confidence

# ----------------------------- Recommendation Generator -----------------------------
def get_recommendations(text):
    emotion, confidence = detect_emotion(text)
    data = emotion_data[emotion]
    return {
        "emotion": emotion,
        "confidence": confidence,
        "videos": random.sample(data["videos"], 3),
        "quote": random.choice(data["quotes"]),
        "affirmation": random.choice(data["affirmations"])
    }

# ----------------------------- Styled Window Display -----------------------------
def show_recommendations(text):
    recs = get_recommendations(text)

    window = tk.Tk()
    window.title("Emotion-Based Recommendations")
    window.geometry("600x400")
    window.configure(bg="#f2f2f2")

    # Scrollable Frame
    canvas = tk.Canvas(window, bg="#f2f2f2", highlightthickness=0)
    frame = tk.Frame(canvas, bg="#f2f2f2")
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_configure)

    # Content
    def add_label(title, content, font=("Helvetica", 11), color="#333"):
        tk.Label(frame, text=title, font=("Helvetica", 12, "bold"), bg="#f2f2f2", fg="#555").pack(anchor="w", pady=(10, 0))
        tk.Label(frame, text=content, font=font, wraplength=550, justify="left", bg="#f2f2f2", fg=color).pack(anchor="w", padx=10)

    add_label("Emotion Detected:", recs["emotion"].capitalize(), font=("Helvetica", 13, "bold"), color="#2c3e50")
    add_label("Confidence:", f"{recs['confidence']:.2f}")
    add_label("Quote:", f'"{recs["quote"]}"')
    add_label("Affirmation:", recs["affirmation"], font=("Helvetica", 11, "italic"), color="#006400")

    tk.Label(frame, text="Recommended Videos:", font=("Helvetica", 12, "bold"), bg="#f2f2f2", fg="#555").pack(anchor="w", pady=(10, 0))
    for link in recs["videos"]:
        video_link = tk.Label(frame, text=link, fg="blue", bg="#f2f2f2", cursor="hand2", wraplength=550)
        video_link.pack(anchor="w", padx=15)
        video_link.bind("<Button-1>", lambda e, url=link: webbrowser.open_new_tab(url))

    window.mainloop()

# Example call
if __name__ == "__main__":
    sample_text = "I feel very anxious and worried lately."
    show_recommendations(sample_text)
