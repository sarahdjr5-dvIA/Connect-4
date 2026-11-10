import tkinter as tk

from AlphaBeta import meilleur_coup_alphabeta as alphabeta_coup
from Board import *
from MinMax import meilleur_coup as minimax_coup
from Solver import *

# dimensions et couleurs
TAILLE_CASE = 75
LARGEUR = NB_COLONNES * TAILLE_CASE
HAUTEUR = 80 + NB_LIGNES * TAILLE_CASE

BLEU = "#385DFF"
JAUNE_C = "#FFDD00"
ROUGE_C = "#FF003C"
BLANC = "white"

partie = initialiser_partie()  # etat initial de la partie

root = tk.Tk()
root.title("Puissance 4 - Selection du Mode & IA")

mode_jeu = tk.IntVar(value=1)  # mode de jeu : 1 = Humain vs Humain, 2 = Minimax, 3 = AlphaBeta


# frame pour choisir le mode de jeu
frame_mode = tk.Frame(root, bg="white", pady=5)
frame_mode.pack(fill="x")

lbl_mode = tk.Label(frame_mode, text="Mode :", font=("Arial", 11, "bold"), bg="white")
lbl_mode.pack(side="left", padx=10)


# reinitialiser la partie
def reset():
    global partie
    partie = initialiser_partie()

    # en mode IA, l'humain (ROUGE) commence
    if mode_jeu.get() in [2, 3]:
        partie["joueur_actuel"] = ROUGE

    dessiner()


# changer le mode de jeu
def changer_mode():
    reset()


# boutons pour choisir le mode de jeu
rb1 = tk.Radiobutton(frame_mode, text="1. Humain vs Humain", variable=mode_jeu, value=1, command=changer_mode, bg="white")
rb1.pack(side="left", padx=5)

rb2 = tk.Radiobutton(frame_mode, text="2. Humain vs Minimax", variable=mode_jeu, value=2, command=changer_mode, bg="white")
rb2.pack(side="left", padx=5)

rb3 = tk.Radiobutton(frame_mode, text="3. Humain vs Alpha-Beta", variable=mode_jeu, value=3, command=changer_mode, bg="white")
rb3.pack(side="left", padx=5)


# canvas pour afficher la grille
canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR, bg="white", highlightthickness=0)
canvas.pack()

label_var = tk.StringVar()  # texte du tour actuel

label = tk.Label(root, textvariable=label_var, font=("Arial", 16, "bold"), bg="white")
label.pack(pady=5)


# mettre a jour le texte du jeu
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


# dessiner la grille et les pions
def dessiner():

    canvas.delete("all")

    # afficher la bande superieure
    canvas.create_rectangle(0, 0, LARGEUR, 80, fill="black", outline="")

    # afficher le fond de la grille
    canvas.create_rectangle(0, 80, LARGEUR, HAUTEUR, fill=BLEU, outline="")

    # parcourir les lignes et les colonnes
    for r in range(NB_LIGNES):

        for c in range(NB_COLONNES):

            x1 = c * TAILLE_CASE + 10
            y1 = 100 + r * TAILLE_CASE + 10
            x2 = x1 + 60
            y2 = y1 + 60

            val = partie["grille"][r][c]  # valeur de la case

            if val == VIDE:
                col = BLANC

            elif val == JAUNE:
                col = JAUNE_C

            else:
                col = ROUGE_C

            canvas.create_oval(x1, y1, x2, y2, fill=col, outline="")

    update_label()


# jouer le tour de l'IA
def tour_ia():

    if partie["terminee"] or partie["joueur_actuel"] != JAUNE:
        return

    update_label()
    root.update_idletasks()

    mode = mode_jeu.get()  # mode de jeu actuel

    if mode == 2:
        col = minimax_coup(partie["grille"])

    elif mode == 3:
        col = alphabeta_coup(partie["grille"])

    else:
        return

    jouer_tour(partie, col)
    dessiner()


# gerer le clic du joueur
def on_click(event):

    if partie["terminee"]:
        return

    # en mode IA, l'humain joue uniquement avec ROUGE
    if mode_jeu.get() in [2, 3] and partie["joueur_actuel"] != ROUGE:
        return

    colonne = event.x // TAILLE_CASE  # colonne cliquee
    res = jouer_tour(partie, colonne)  # resultat du coup

    if res in ["COUP_VALIDE", "VICTOIRE", "MATCH_NUL"]:

        dessiner()

        # lancer le tour de l'IA apres le tour humain
        if not partie["terminee"] and mode_jeu.get() in [2, 3] and partie["joueur_actuel"] == JAUNE:

            label_var.set("Tour : IA (JAUNE reflexion...)")
            root.update_idletasks()
            root.after(200, tour_ia)


canvas.bind("<Button-1>", on_click)  # detecter le clic sur la grille

dessiner()  # afficher la grille initiale

root.mainloop()  # lancer la fenetre
