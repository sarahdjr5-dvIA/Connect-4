from Board import *
from Solver import *
from MinMax import *


# ============================================================
# TEST 1 : GRILLE VIDE
# ============================================================

print("========================================")
print("TEST 1 : GRILLE VIDE")
print("========================================")

grille = creer_grille()

colonne = meilleur_coup(grille)

print("Meilleur coup :", colonne)


# ============================================================
# TEST 2 : JAUNE PEUT GAGNER
# ============================================================

print()
print("========================================")
print("TEST 2 : JAUNE DOIT GAGNER")
print("========================================")

grille = creer_grille()

# Mettre trois pions JAUNE dans les colonnes 0, 1 et 2
placer_pion(grille, 0, JAUNE)
placer_pion(grille, 1, JAUNE)
placer_pion(grille, 2, JAUNE)

print("Grille :")

for ligne in grille:
    print(ligne)

colonne = meilleur_coup(grille)

print()
print("Meilleur coup :", colonne)
print("Coup attendu : 3")


# ============================================================
# TEST 3 : JAUNE DOIT BLOQUER ROUGE
# ============================================================

print()
print("========================================")
print("TEST 3 : JAUNE DOIT BLOQUER ROUGE")
print("========================================")

grille = creer_grille()

# ROUGE a trois pions consecutifs
placer_pion(grille, 0, ROUGE)
placer_pion(grille, 1, ROUGE)
placer_pion(grille, 2, ROUGE)

print("Grille :")

for ligne in grille:
    print(ligne)

colonne = meilleur_coup(grille)

print()
print("Meilleur coup :", colonne)
print("Coup attendu : 3")