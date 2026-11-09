
from Board import *
from Solver import *

from Minimax import (
    coups_possibles,
    simuler_coup,
    evaluer_grille,
    MAX_DEPTH,
    WIN_SCORE
)


#fonction alphabeta qui cherche le meilleur coup en eliminant les branches inutiles

def alphabeta(grille, profondeur, alpha, beta, maximisant):

    coups = coups_possibles(grille)  #les colonnes ou on peut encore jouer

    #on verifie si un joueur a gagné ou si la grille est pleine

    if verifier_victoire(grille, JAUNE):
        return WIN_SCORE - profondeur, None  #on favorise une victoire rapide de JAUNE

    if verifier_victoire(grille, ROUGE):
        return -WIN_SCORE + profondeur  , None  #on favorise une defaite plus tardive de JAUNE

    if grille_pleine(grille):
        return 0, None  #match nul

    #si on atteint la profondeur maximale on evalue la grille avec l'heuristique

    if profondeur == MAX_DEPTH:
        return evaluer_grille(grille), None

    #si c'est le tour de JAUNE (MAX)

    if maximisant:

        meilleure_valeur = float("-inf")  #meilleure valeur trouvée
        meilleur_coup = coups[0]  #premiere colonne possible

        #on teste tous les coups possibles de JAUNE

        for colonne in coups:

            nouvelle_grille = simuler_coup(grille, colonne, JAUNE)  #on simule le coup de JAUNE

            valeur, _ = alphabeta(nouvelle_grille, profondeur + 1, alpha, beta, False)  #on passe au tour de ROUGE

            if valeur > meilleure_valeur:
                meilleure_valeur = valeur  #on garde la meilleure valeur
                meilleur_coup = colonne  #on garde la colonne correspondante

            if meilleure_valeur > alpha:
                alpha = meilleure_valeur  #on met a jour alpha

            if beta <= alpha:
                break  #on arrete de tester les autres coups car ils sont inutiles

        return meilleure_valeur, meilleur_coup

    #sinon c'est le tour de ROUGE (MIN)

    else:

        meilleure_valeur = float("inf")  #meilleure valeur trouvée
        meilleur_coup = coups[0]  #premiere colonne possible

        #on teste tous les coups possibles de ROUGE

        for colonne in coups:

            nouvelle_grille = simuler_coup(grille, colonne, ROUGE)  #on simule le coup de ROUGE

            valeur, _ = alphabeta(nouvelle_grille, profondeur + 1, alpha, beta, True)  #on passe au tour de JAUNE

            if valeur < meilleure_valeur:
                meilleure_valeur = valeur  #on garde la plus petite valeur
                meilleur_coup = colonne  #on garde la colonne correspondante

            if meilleure_valeur < beta:
                beta = meilleure_valeur  #on met a jour beta

            if beta <= alpha:
                break  #on arrete de tester les autres coups car ils sont inutiles

        return meilleure_valeur, meilleur_coup


#fonction qui cherche le meilleur coup pour l'ordinateur (JAUNE)

def meilleur_coup_alphabeta(grille):

    #on commence la recherche avec alpha = -infini et beta = +infini

    valeur, colonne = alphabeta(
        grille,
        0,
        float("-inf"),
        float("inf"),
        True
    )

    return colonne  #on retourne la colonne choisie par l'ordinateur
