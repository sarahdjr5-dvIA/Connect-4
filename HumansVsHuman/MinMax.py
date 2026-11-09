
# ============================================================
# MINIMAX - PUISSANCE 4
# ============================================================

from Board import *
from Solver import *


# ============================================================
# PARAMETRES
# ============================================================

# Profondeur maximale de recherche
MAX_DEPTH = 4

# Valeur tres grande utilisee pour representer une victoire
WIN_SCORE = 100000


# ============================================================
# COUPS POSSIBLES
# ============================================================

def coups_possibles(grille):
    """
    Retourne la liste des colonnes dans lesquelles
    un pion peut encore etre place.
    """

    coups = []

    for colonne in range(NB_COLONNES):

        if not colonne_pleine(grille, colonne):

            coups.append(colonne)

    return coups


# ============================================================
# COPIE DE LA GRILLE
# ============================================================

def copier_grille(grille):
    """
    Cree une copie independante de la grille.

    On en a besoin parce que Minimax doit pouvoir
    essayer des coups sans modifier la vraie grille.
    """

    nouvelle_grille = []

    for ligne in grille:

        nouvelle_grille.append(ligne[:])

    return nouvelle_grille


# ============================================================
# SIMULATION D'UN COUP
# ============================================================

def simuler_coup(grille, colonne, joueur):
    """
    Simule le placement d'un pion dans une copie
    de la grille.

    La grille originale n'est pas modifiee.
    """

    nouvelle_grille = copier_grille(grille)

    placer_pion(nouvelle_grille, colonne, joueur)

    return nouvelle_grille


# ============================================================
# EVALUATION D'UNE FENETRE DE 4 CASES
# ============================================================

def evaluer_fenetre(fenetre):
    """
    Evalue une fenetre de 4 cases.

    JAUNE = joueur MAX = ordinateur
    ROUGE = joueur MIN = humain
    """

    score = 0

    # Compter les cases de chaque type
    nb_jaune = fenetre.count(JAUNE)
    nb_rouge = fenetre.count(ROUGE)
    nb_vide = fenetre.count(VIDE)

    # --------------------------------------------------------
    # Evaluation pour JAUNE
    # --------------------------------------------------------

    if nb_jaune == 4:

        score += WIN_SCORE

    elif nb_jaune == 3 and nb_vide == 1:

        score += 5

    elif nb_jaune == 2 and nb_vide == 2:

        score += 2

    # --------------------------------------------------------
    # Evaluation pour ROUGE
    # --------------------------------------------------------

    if nb_rouge == 4:

        score -= WIN_SCORE

    elif nb_rouge == 3 and nb_vide == 1:

        score -= 5

    elif nb_rouge == 2 and nb_vide == 2:

        score -= 2

    return score


# ============================================================
# HEURISTIQUE B
# ============================================================

def evaluer_grille(grille):
    """
    Evalue l'ensemble de la grille.

    L'evaluation est faite en examinant toutes les
    fenetres possibles de 4 cases :

    - horizontalement
    - verticalement
    - diagonalement \
    - diagonalement /

    Un score positif est favorable a JAUNE.
    Un score negatif est favorable a ROUGE.
    """

    score = 0

    # --------------------------------------------------------
    # HORIZONTAL
    # --------------------------------------------------------

    for ligne in range(NB_LIGNES):

        for colonne in range(NB_COLONNES - 3):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne][colonne + 1],
                grille[ligne][colonne + 2],
                grille[ligne][colonne + 3]
            ]

            score += evaluer_fenetre(fenetre)

    # --------------------------------------------------------
    # VERTICAL
    # --------------------------------------------------------

    for ligne in range(NB_LIGNES - 3):

        for colonne in range(NB_COLONNES):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne + 1][colonne],
                grille[ligne + 2][colonne],
                grille[ligne + 3][colonne]
            ]

            score += evaluer_fenetre(fenetre)

    # --------------------------------------------------------
    # DIAGONALE DESCENDANTE \
    # --------------------------------------------------------

    for ligne in range(NB_LIGNES - 3):

        for colonne in range(NB_COLONNES - 3):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne + 1][colonne + 1],
                grille[ligne + 2][colonne + 2],
                grille[ligne + 3][colonne + 3]
            ]

            score += evaluer_fenetre(fenetre)

    # --------------------------------------------------------
    # DIAGONALE MONTANTE /
    # --------------------------------------------------------

    for ligne in range(3, NB_LIGNES):

        for colonne in range(NB_COLONNES - 3):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne - 1][colonne + 1],
                grille[ligne - 2][colonne + 2],
                grille[ligne - 3][colonne + 3]
            ]

            score += evaluer_fenetre(fenetre)

    # --------------------------------------------------------
    # BONUS POUR LA COLONNE CENTRALE
    # --------------------------------------------------------

    colonne_centrale = NB_COLONNES // 2

    for ligne in range(NB_LIGNES):

        if grille[ligne][colonne_centrale] == JAUNE:

            score += 3

        elif grille[ligne][colonne_centrale] == ROUGE:

            score -= 3

    return score


# ============================================================
# MINIMAX
# ============================================================

def minimax(grille, profondeur, maximisant):
    """
    Algorithme Minimax.

    Parametres :
        grille      : etat actuel du plateau
        profondeur  : profondeur actuelle dans l'arbre
        maximisant  : True si c'est le tour de JAUNE,
                      False si c'est le tour de ROUGE

    Retourne :
        (meilleure_valeur, meilleur_coup)
    """

    # --------------------------------------------------------
    # Recuperer les coups possibles
    # --------------------------------------------------------

    coups = coups_possibles(grille)

    # --------------------------------------------------------
    # VERIFICATION DES ETATS TERMINAUX
    # --------------------------------------------------------

    # JAUNE a gagne
    if verifier_victoire(grille, JAUNE):

        return WIN_SCORE - profondeur, None

    # ROUGE a gagne
    if verifier_victoire(grille, ROUGE):

        return -WIN_SCORE + profondeur, None

    # Match nul
    if grille_pleine(grille):

        return 0, None

    # --------------------------------------------------------
    # LIMITE DE PROFONDEUR
    # --------------------------------------------------------

    if profondeur == MAX_DEPTH:

        return evaluer_grille(grille), None

    # ========================================================
    # CAS MAX
    # ========================================================

    if maximisant:

        # Au debut, aucune valeur n'est encore connue
        meilleure_valeur = float("-inf")

        # On prend le premier coup comme coup par defaut
        meilleur_coup = coups[0]

        # Tester tous les coups possibles
        for colonne in coups:

            # Simuler le coup de JAUNE
            nouvelle_grille = simuler_coup(
                grille,
                colonne,
                JAUNE
            )

            # Appeler Minimax pour le niveau suivant
            valeur, _ = minimax(
                nouvelle_grille,
                profondeur + 1,
                False
            )

            # Garder la meilleure valeur
            if valeur > meilleure_valeur:

                meilleure_valeur = valeur
                meilleur_coup = colonne

        return meilleure_valeur, meilleur_coup

    # ========================================================
    # CAS MIN
    # ========================================================

    else:

        # Au debut, aucune valeur n'est encore connue
        meilleure_valeur = float("inf")

        # Coup par defaut
        meilleur_coup = coups[0]

        # Tester tous les coups possibles
        for colonne in coups:

            # Simuler le coup de ROUGE
            nouvelle_grille = simuler_coup(
                grille,
                colonne,
                ROUGE
            )

            # Appeler Minimax pour le niveau suivant
            valeur, _ = minimax(
                nouvelle_grille,
                profondeur + 1,
                True
            )

            # Garder la plus petite valeur
            if valeur < meilleure_valeur:

                meilleure_valeur = valeur
                meilleur_coup = colonne

        return meilleure_valeur, meilleur_coup


# ============================================================
# RECHERCHE DU MEILLEUR COUP
# ============================================================

def meilleur_coup(grille):
    """
    Determine le meilleur coup pour JAUNE.

    JAUNE est le joueur controle par l'ordinateur.
    """

    valeur, colonne = minimax(
        grille,
        0,
        True
    )

    return colonne
