from Board import *
from Solver import *

MAX_DEPTH = 4       # profondeur maximale de recherche
WIN_SCORE = 100000  # valeur tres grande pour representer une victoire


def coups_possibles(grille):
    coups = []  # liste des colonnes possibles

    for colonne in range(NB_COLONNES):
        if not colonne_pleine(grille, colonne):
            coups.append(colonne)

    return coups


def copier_grille(grille):
    nouvelle_grille = []  # copie de la grille

    for ligne in grille:
        nouvelle_grille.append(ligne[:])

    return nouvelle_grille


def simuler_coup(grille, colonne, joueur):
    nouvelle_grille = copier_grille(grille)  # copie de la grille
    placer_pion(nouvelle_grille, colonne, joueur)  # placer le pion dans la copie

    return nouvelle_grille


def evaluer_fenetre(fenetre):
    score = 0  # score de la fenetre

    # on compte les cases de chaque type
    nb_jaune = fenetre.count(JAUNE)  # nombre de pions jaunes
    nb_rouge = fenetre.count(ROUGE)  # nombre de pions rouges
    nb_vide = fenetre.count(VIDE)    # nombre de cases vides

    # evaluation pour JAUNE
    if nb_jaune == 4:
        score += WIN_SCORE

    elif nb_jaune == 3 and nb_vide == 1:
        score += 5

    elif nb_jaune == 2 and nb_vide == 2:
        score += 2

    # evaluation pour ROUGE
    if nb_rouge == 4:
        score -= WIN_SCORE

    elif nb_rouge == 3 and nb_vide == 1:
        score -= 5

    elif nb_rouge == 2 and nb_vide == 2:
        score -= 2

    return score


def evaluer_grille(grille):
    score = 0  # score total de la grille

    # on verifie horizontalement
    for ligne in range(NB_LIGNES):
        for colonne in range(NB_COLONNES - 3):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne][colonne + 1],
                grille[ligne][colonne + 2],
                grille[ligne][colonne + 3]
            ]

            score += evaluer_fenetre(fenetre)

    # on verifie verticalement
    for ligne in range(NB_LIGNES - 3):
        for colonne in range(NB_COLONNES):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne + 1][colonne],
                grille[ligne + 2][colonne],
                grille[ligne + 3][colonne]
            ]

            score += evaluer_fenetre(fenetre)

    # on verifie les diagonales descendantes
    for ligne in range(NB_LIGNES - 3):
        for colonne in range(NB_COLONNES - 3):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne + 1][colonne + 1],
                grille[ligne + 2][colonne + 2],
                grille[ligne + 3][colonne + 3]
            ]

            score += evaluer_fenetre(fenetre)

    # on verifie les diagonales montantes
    for ligne in range(3, NB_LIGNES):
        for colonne in range(NB_COLONNES - 3):

            fenetre = [
                grille[ligne][colonne],
                grille[ligne - 1][colonne + 1],
                grille[ligne - 2][colonne + 2],
                grille[ligne - 3][colonne + 3]
            ]

            score += evaluer_fenetre(fenetre)

    # on ajoute un bonus pour la colonne centrale
    colonne_centrale = NB_COLONNES // 2  # indice de la colonne centrale

    for ligne in range(NB_LIGNES):
        if grille[ligne][colonne_centrale] == JAUNE:
            score += 3

        elif grille[ligne][colonne_centrale] == ROUGE:
            score -= 3

    return score


def minimax(grille, profondeur, maximisant):
    coups = coups_possibles(grille)  # liste des coups possibles

    # on verifie si JAUNE a gagne
    if verifier_victoire(grille, JAUNE):
        return WIN_SCORE - profondeur, None

    # on verifie si ROUGE a gagne
    if verifier_victoire(grille, ROUGE):
        return -WIN_SCORE + profondeur, None

    # on verifie si la grille est pleine
    if grille_pleine(grille):
        return 0, None

    # on arrete la recherche si la profondeur maximale est atteinte
    if profondeur == MAX_DEPTH:
        return evaluer_grille(grille), None

    # cas MAX
    if maximisant:
        meilleure_valeur = float("-inf")  # valeur initiale tres petite
        meilleur_coup = coups[0]  # premier coup par defaut

        # on teste tous les coups possibles
        for colonne in coups:

            # on simule le coup de JAUNE
            nouvelle_grille = simuler_coup(grille, colonne, JAUNE)

            # on passe au niveau suivant avec ROUGE
            valeur, _ = minimax(nouvelle_grille, profondeur + 1, False)

            # on garde la plus grande valeur
            if valeur > meilleure_valeur:
                meilleure_valeur = valeur
                meilleur_coup = colonne

        return meilleure_valeur, meilleur_coup

    # cas MIN
    else:
        meilleure_valeur = float("inf")  # valeur initiale tres grande
        meilleur_coup = coups[0]  # premier coup par defaut

        # on teste tous les coups possibles
        for colonne in coups:

            # on simule le coup de ROUGE
            nouvelle_grille = simuler_coup(grille, colonne, ROUGE)

            # on passe au niveau suivant avec JAUNE
            valeur, _ = minimax(nouvelle_grille, profondeur + 1, True)

            # on garde la plus petite valeur
            if valeur < meilleure_valeur:
                meilleure_valeur = valeur
                meilleur_coup = colonne

        return meilleure_valeur, meilleur_coup


def meilleur_coup(grille):
    # on lance Minimax avec JAUNE depuis la profondeur 0
    valeur, colonne = minimax(grille, 0, True)

    return colonne
