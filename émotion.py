import tkinter as tk
from tkinter import messagebox
from pushbullet import Pushbullet

# ===============================
# CONFIG PUSHBULLET
# ===============================
ACCESS_TOKEN = "o.DAOy0rXU88s8JXtSs4JT7hBdqXecLPAm"
pb = Pushbullet(ACCESS_TOKEN)

# ===============================
# QUESTIONS
# ===============================
questions = [
    ("Comment te sens-tu aujourd’hui ?", [
        ("😄 Super bien", 2),
        ("🙂 Bien", 1),
        ("😕 Bof", -1),
        ("😢 Pas bien", -2)
    ]),
    ("As-tu bien dormi ?", [
        ("😴 Comme un bébé", 2),
        ("🙂 Correct", 0),
        ("🥱 Mal dormi", -2)
    ]),
    ("Ton niveau de stress ?", [
        ("🧘 Aucun stress", 2),
        ("😐 Un peu", 0),
        ("😖 Beaucoup", -2)
    ]),
    ("As-tu mangé aujourd’hui ?", [
        ("🍎 Équilibré", 1),
        ("🍔 Pas top", -1)
    ]),
    ("As-tu bougé un peu ?", [
        ("🏃 Oui", 1),
        ("🛋️ Non", -1)
    ]),
    ("As-tu ri aujourd’hui ?", [
        ("😂 Oui beaucoup", 2),
        ("🙂 Un peu", 1),
        ("😐 Pas vraiment", -1)
    ]),
    ("Ton énergie est plutôt :", [
        ("⚡ Haute", 2),
        ("🔋 Moyenne", 0),
        ("🪫 Basse", -2)
    ]),
    ("As-tu parlé à quelqu’un ?", [
        ("💬 Oui", 1),
        ("🙈 Non", -1)
    ]),
    ("Te sens-tu motivé(e) ?", [
        ("🔥 À fond", 2),
        ("🙂 Moyen", 0),
        ("😴 Pas du tout", -2)
    ]),
    ("As-tu pris du temps pour toi ?", [
        ("🛀 Oui", 1),
        ("❌ Non", -1)
    ]),
    ("Comment est ton moral ?", [
        ("🌈 Très bon", 2),
        ("🙂 Correct", 0),
        ("🌧️ Pas top", -2)
    ]),
    ("As-tu été fier(e) de toi ?", [
        ("🏆 Oui", 2),
        ("😐 Bof", 0),
        ("😔 Non", -2)
    ]),
    ("As-tu aidé quelqu’un ?", [
        ("🤝 Oui", 1),
        ("❌ Non", 0)
    ]),
    ("Te sens-tu entouré(e) ?", [
        ("❤️ Oui", 2),
        ("😐 Un peu", 0),
        ("💔 Non", -2)
    ]),
    ("Ta journée était :", [
        ("🌞 Géniale", 2),
        ("🌤️ Correcte", 0),
        ("🌪️ Difficile", -2)
    ])
]

# ===============================
# VARIABLES
# ===============================
index = 0
score = 0
resume = []

# ===============================
# FONCTIONS
# ===============================
def repondre(points, texte):
    global index, score
    score += points
    resume.append(f"- {questions[index][0]} → {texte}")
    index += 1

    if index < len(questions):
        afficher_question()
    else:
        afficher_resultat()

def afficher_question():
    question_label.config(text=f"❓ {questions[index][0]}")
    for widget in frame_btn.winfo_children():
        widget.destroy()

    progress_label.config(
        text=f"Question {index + 1} / {len(questions)}"
    )

    for texte, points in questions[index][1]:
        btn = tk.Button(
            frame_btn,
            text=texte,
            font=("Arial", 12),
            width=30,
            command=lambda p=points, t=texte: repondre(p, t)
        )
        btn.pack(pady=4)

def afficher_resultat():
    fenetre.destroy()

    if score >= 15:
        emotion = "😄 Très heureux"
        message = "Excellente journée 🌈"
    elif score >= 7:
        emotion = "🙂 Bien"
        message = "Globalement ça va 👍"
    elif score >= 0:
        emotion = "😐 Moyen"
        message = "Journée mitigée"
    elif score >= -7:
        emotion = "😟 Difficile"
        message = "Pas facile aujourd’hui"
    else:
        emotion = "😢 Très difficile"
        message = "Besoin de soutien ❤️"

    contenu = (
        f"BILAN DU JOUR\n\n"
        f"Score : {score}\n"
        f"Émotion : {emotion}\n\n"
        + "\n".join(resume)
    )

    pb.push_note("Quiz bien-être", contenu)

    messagebox.showinfo(
        "Résultat",
        f"{emotion}\n\n{message}\n\n📱 Notification envoyée"
    )

# ===============================
# INTERFACE TKINTER
# ===============================
fenetre = tk.Tk()
fenetre.title("🧠 Quiz Bien-Être Fun")
fenetre.geometry("520x450")
fenetre.resizable(False, False)

question_label = tk.Label(
    fenetre,
    text="",
    font=("Arial", 14),
    wraplength=480,
    justify="center"
)
question_label.pack(pady=20)

progress_label = tk.Label(
    fenetre,
    text="",
    font=("Arial", 10)
)
progress_label.pack()

frame_btn = tk.Frame(fenetre)
frame_btn.pack(pady=20)

afficher_question()

fenetre.mainloop()
