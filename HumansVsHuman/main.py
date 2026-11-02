import tkinter as tk
from Solver import *

TAILLE_CASE = 75
LARGEUR = NB_COLONNES * TAILLE_CASE
HAUTEUR = 80 + NB_LIGNES * TAILLE_CASE

BLEU = "#385DFF"
JAUNE_C = "#FFDD00"
ROUGE_C = "#FF003C"
BLANC = "white"

partie = initialiser_partie()

root = tk.Tk()
root.title("Puissance 4")

canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR, bg="white", highlightthickness=0)
canvas.pack()

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var, font=("Arial", 18, "bold"))
label.pack()

def update_label():
    if partie["terminee"]:
        if partie["gagnant"] != VIDE:
            nom = "JAUNE" if partie["gagnant"] == JAUNE else "ROUGE"
            label_var.set(f"Victoire {nom} !")
        else:
            label_var.set("Match nul !")
    else:
        nom = "JAUNE" if partie["joueur_actuel"] == JAUNE else "ROUGE"
        label_var.set(f"Tour: {nom}")

def dessiner():
    canvas.delete("all")
    # top bar
    canvas.create_rectangle(0, 0, LARGEUR, 80, fill="black", outline="")
    # blue board
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

def on_click(event):
    if partie["terminee"]:
        return
    colonne = event.x // TAILLE_CASE
    jouer_tour(partie, colonne)
    dessiner()

canvas.bind("<Button-1>", on_click)

def reset():
    global partie
    partie = initialiser_partie()
    dessiner()

btn = tk.Button(root, text="Recommencer", command=reset, font=("Arial", 12))
btn.pack(pady=5)

dessiner()
root.mainloop()