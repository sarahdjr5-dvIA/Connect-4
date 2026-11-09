# ============================================================
# DEFINITION DE LA GRILLE
# ============================================================

NB_LIGNES = 6
NB_COLONNES = 7

VIDE = 0
JAUNE = 1
ROUGE = 2

NB_PIONS_GAGNANTS = 4


# ============================================================
# CREATION DE LA GRILLE
# ============================================================

def creer_grille():
    # Creer une matrice de 6 lignes et 7 colonnes remplie de 0
    grille = []

    for i in range(NB_LIGNES):
        ligne = []

        for j in range(NB_COLONNES):
            ligne.append(VIDE)

        grille.append(ligne)

    return grille