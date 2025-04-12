from fpdf import FPDF
import matplotlib.pyplot as plt
from collections import Counter
import re
import os
from datetime import datetime
import random

# 📁 Path to the journal entry file
ENTRY_FILE_PATH = r"C:\Users\dadia\OneDrive\Desktop\entries.txt.txt"

# ---------------- EMOTION CLASSIFIER (Dummy) ----------------
def simple_emotion_classifier(text):
    text = text.lower()
    if any(w in text for w in ['stress', 'pressur', 'anxious', 'worried']):
        return "Stressed"
    elif any(w in text for w in ['happy', 'good', 'great', 'joy']):
        return "Happy"
    elif any(w in text for w in ['calm', 'peace', 'relax']):
        return "Calm"
    elif any(w in text for w in ['angry', 'mad', 'irritated']):
        return "Angry"
    elif any(w in text for w in ['sad', 'down', 'low', 'upset']):
        return "Sad"
    else:
        return random.choice(["Neutral", "Okay", "Mixed"])

# ---------------- PARSE ENTRIES FROM TXT FILE ----------------
def load_entries_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        raw = file.read()

    entry_blocks = [e.strip() for e in raw.split("="*50) if e.strip()]
    journal_data = {}

    for block in entry_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue

        timestamp_line = lines[0].strip()
        content = "\n".join(lines[1:]).strip()

        try:
            timestamp = datetime.strptime(timestamp_line.strip('[]'), "%Y-%m-%d %H:%M:%S")
            date_str = timestamp.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"⚠️ Skipping invalid block: {e}")
            continue

        emotion = simple_emotion_classifier(content)
        entry_obj = {"content": content, "emotion": emotion}

        journal_data.setdefault(date_str, []).append(entry_obj)

    return journal_data

# ---------------- WORD FREQUENCY CHART ----------------
def generate_word_frequency_chart(entries, output_path='word_frequency.png'):
    all_text = " ".join(entries).lower()
    words = re.findall(r'\b[a-z]{3,}\b', all_text)
    stopwords = {'the', 'and', 'for', 'are', 'with', 'that', 'you', 'your', 'from', 'have', 'this', 'but'}
    filtered_words = [word for word in words if word not in stopwords]

    word_counts = Counter(filtered_words)
    most_common = word_counts.most_common(10)

    if not most_common:
        return None

    words, counts = zip(*most_common)
    plt.figure(figsize=(8, 5))
    plt.bar(words, counts, color='cyan')
    plt.title("Top 10 Frequent Words")
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- PDF CLASS ----------------
class JournalPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 128, 128)
        self.cell(0, 10, "Mental Health Journal Report", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.set_text_color(100)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", align='C')

    def add_day_summary(self, date, entries):
        self.set_font("Arial", "B", 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, f"Date: {date}", ln=True)
        self.set_font("Arial", "", 11)

        for entry in entries:
            self.multi_cell(0, 8, f"- {entry['content']} (Emotion: {entry['emotion']})", align='L')
        self.ln(4)

# ---------------- REPORT GENERATOR ----------------
def generate_report(data, filename="mental_health_report.pdf"):
    pdf = JournalPDF()
    pdf.add_page()

    all_texts = []
    for date, entries in data.items():
        pdf.add_day_summary(date, entries)
        all_texts.extend([entry["content"] for entry in entries])

    chart_path = generate_word_frequency_chart(all_texts)
    if chart_path:
        pdf.image(chart_path, x=30, w=150)

    pdf.output(filename)
    if os.path.exists(chart_path):
        os.remove(chart_path)
    print(f"✅ Report saved as {filename}")

# ---------------- RUN IT ALL ----------------
journal_data = load_entries_from_file(ENTRY_FILE_PATH)
if journal_data:
    generate_report(journal_data)
else:
    print("🚫 No entries found to generate report.")
