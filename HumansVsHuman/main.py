import tkinter as tk
from Board import *
from Solver import *
from MinMax import meilleur_coup as minimax_coup
from AlphaBeta import meilleur_coup_alphabeta as alphabeta_coup
# Dimensions & Colors
TAILLE_CASE = 75
LARGEUR = NB_COLONNES * TAILLE_CASE
HAUTEUR = 80 + NB_LIGNES * TAILLE_CASE

BLEU = "#385DFF"
JAUNE_C = "#FFDD00"
ROUGE_C = "#FF003C"
BLANC = "white"

# Game state initialization
partie = initialiser_partie()

root = tk.Tk()
root.title("Puissance 4 - Selection du Mode & IA")

# 1: Humain vs Humain, 2: Humain vs Minimax, 3: Humain vs AlphaBeta
mode_jeu = tk.IntVar(value=1)

# ============================================================
# TOP FRAME: MODE SELECTION
# ============================================================
frame_mode = tk.Frame(root, bg="white", pady=5)
frame_mode.pack(fill="x")

lbl_mode = tk.Label(frame_mode, text="Mode :", font=("Arial", 11, "bold"), bg="white")
lbl_mode.pack(side="left", padx=10)

def reset():
    global partie
    partie = initialiser_partie()
    dessiner()

def changer_mode():
    reset()

rb1 = tk.Radiobutton(frame_mode, text="1. Humain vs Humain", variable=mode_jeu, value=1, command=changer_mode, bg="white")
rb1.pack(side="left", padx=5)

rb2 = tk.Radiobutton(frame_mode, text="2. Humain vs Minimax", variable=mode_jeu, value=2, command=changer_mode, bg="white")
rb2.pack(side="left", padx=5)

rb3 = tk.Radiobutton(frame_mode, text="3. Humain vs Alpha-Beta", variable=mode_jeu, value=3, command=changer_mode, bg="white")
rb3.pack(side="left", padx=5)

# ============================================================
# CANVAS & LABELS
# ============================================================
canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR, bg="white", highlightthickness=0)
canvas.pack()

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var, font=("Arial", 16, "bold"), bg="white")
label.pack(pady=5)

def update_label():
    if partie["terminee"]:
        if partie["gagnant"] != VIDE:
            if mode_jeu.get() == 1:
                nom = "JAUNE" if partie["gagnant"] == JAUNE else "ROUGE"
            else:
                nom = "IA (JAUNE)" if partie["gagnant"] == JAUNE else "Humain (ROUGE)"
            label_var.set(f"Victoire {nom} !")
        else:
            label_var.set("Match nul !")
    else:
        if mode_jeu.get() == 1:
            nom = "JAUNE" if partie["joueur_actuel"] == JAUNE else "ROUGE"
            label_var.set(f"Tour : {nom}")
        else:
            if partie["joueur_actuel"] == ROUGE:
                label_var.set("Tour : Humain (ROUGE)")
            else:
                label_var.set("Tour : IA (JAUNE reflexion...)")

def dessiner():
    canvas.delete("all")
    # Top banner
    canvas.create_rectangle(0, 0, LARGEUR, 80, fill="black", outline="")
    # Grid background
    canvas.create_rectangle(0, 80, LARGEUR, HAUTEUR, fill=BLEU, outline="")

    for r in range(NB_LIGNES):
        for c in range(NB_COLONNES):
            x1 = c * TAILLE_CASE + 10
            y1 = 100 + r * TAILLE_CASE + 10
            x2 = x1 + 60
            y2 = y1 + 60

            val = partie["grille"][r][c]
            if val == VIDE:
                col = BLANC
            elif val == JAUNE:
                col = JAUNE_C
            else:
                col = ROUGE_C

            canvas.create_oval(x1, y1, x2, y2, fill=col, outline="")

    update_label()

# ============================================================
# AI TURN LOGIC
# ============================================================
def tour_ia():
    if partie["terminee"] or partie["joueur_actuel"] != JAUNE:
        return

    mode = mode_jeu.get()
    if mode == 2:
        col = minimax_coup(partie["grille"])
    elif mode == 3:
        col = alphabeta_coup(partie["grille"])
    else:
        return

    jouer_tour(partie, col)
    dessiner()

# ============================================================
# PLAYER CLICK EVENT
# ============================================================
def on_click(event):
    if partie["terminee"]:
        return

    # Against AI, only Human (ROUGE) clicks
    if mode_jeu.get() != 1 and partie["joueur_actuel"] != ROUGE:
        return

    colonne = event.x // TAILLE_CASE
    res = jouer_tour(partie, colonne)

    if res in ["COUP_VALIDE", "VICTOIRE", "MATCH_NUL"]:
        dessiner()

        # Trigger AI move after human turn
        if not partie["terminee"] and mode_jeu.get() in [2, 3] and partie["joueur_actuel"] == JAUNE:
            root.after(300, tour_ia)

canvas.bind("<Button-1>", on_click)

# Start
dessiner()
root.mainloop()