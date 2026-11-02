
# Dimensions de la grille
NB_LIGNES = 6
NB_COLONNES = 7

# Valeurs des joueurs
VIDE = 0
JAUNE = 1
ROUGE = 2

# Nombre de pions necessaires pour gagner
NB_PIONS_GAGNANTS = 4

#INITIALISATION DE LA PARTIE

def creer_grille():
    # Creer une matrice de 6 lignes et 7 colonnes remplie de 0
    grille = []

    for i in range(NB_LIGNES):
        ligne = []

        for j in range(NB_COLONNES):
            ligne.append(VIDE)

        grille.append(ligne)

    return grille


def initialiser_partie():
    # Creer une nouvelle partie
    partie = {
        "grille": creer_grille(),
        "joueur_actuel": JAUNE,
        "gagnant": VIDE,
        "terminee": False
    }

    return partie


def colonne_valide(colonne):
    # Verifier si le numero de colonne existe
    return not (colonne < 0 or colonne >= NB_COLONNES)


def colonne_pleine(grille, colonne):
    # Une colonne est pleine si sa premiere case est occupee
    return grille[0][colonne] != VIDE


# PLACEMENT D'UN PION

def placer_pion(grille, colonne, joueur):
    # Verifier si la colonne est valide
    if not colonne_valide(colonne):
        return False

    # Verifier si la colonne est pleine
    if colonne_pleine(grille, colonne):
        return False

    # Parcourir la colonne de bas en haut
    for ligne in range(NB_LIGNES - 1, -1, -1):

        # Chercher la premiere case vide
        if grille[ligne][colonne] == VIDE:

            # Placer le pion du joueur
            grille[ligne][colonne] = joueur

            return True

    return False

#VERIFICATION DE LA VICTOIRE

def verifier_horizontal(grille, joueur):

    # Parcourir toutes les lignes
    for ligne in range(NB_LIGNES):

        # Parcourir les colonnes possibles
        for colonne in range(NB_COLONNES - 3):

            # Verifier 4 cases consecutives horizontalement
            if (grille[ligne][colonne] == joueur and
                grille[ligne][colonne + 1] == joueur and
                grille[ligne][colonne + 2] == joueur and
                grille[ligne][colonne + 3] == joueur):

                return True

    return False


def verifier_vertical(grille, joueur):

    # Parcourir les lignes possibles
    for ligne in range(NB_LIGNES - 3):

        # Parcourir toutes les colonnes
        for colonne in range(NB_COLONNES):

            # Verifier 4 cases consecutives verticalement
            if (grille[ligne][colonne] == joueur and
                grille[ligne + 1][colonne] == joueur and
                grille[ligne + 2][colonne] == joueur and
                grille[ligne + 3][colonne] == joueur):

                return True

    return False


def verifier_diagonale(grille, joueur):

    # Parcourir les lignes et colonnes possibles
    for ligne in range(NB_LIGNES - 3):
        for colonne in range(NB_COLONNES - 3):

            # Verifier une diagonale descendante vers la droite
            if (grille[ligne][colonne] == joueur and
                grille[ligne + 1][colonne + 1] == joueur and
                grille[ligne + 2][colonne + 2] == joueur and
                grille[ligne + 3][colonne + 3] == joueur):

                return True

    return False

def verifier_victoire(grille, joueur):

    # Verifier les 4 directions possibles
    if verifier_horizontal(grille, joueur):
        return True

    if verifier_vertical(grille, joueur):
        return True

    if verifier_diagonale(grille, joueur):
        return True

    
#VERIFICATION DE LA GRILLE

def grille_pleine(grille):

    # Verifier si toutes les cases sont occupees
    for colonne in range(NB_COLONNES):

        if grille[0][colonne] == VIDE:
            return False

    return True

#CHANGEMENT DE JOUEUR

def changer_joueur(joueur):

    # Si le joueur actuel est jaune, passer au rouge
    if joueur == JAUNE:
        return ROUGE

    # Sinon, passer au jaune
    return JAUNE


#JOUER UN TOUR

def jouer_tour(partie, colonne):

    # Verifier si la partie est deja terminee
    if partie["terminee"]:
        return "PARTIE_TERMINEE"

    grille = partie["grille"]
    joueur = partie["joueur_actuel"]

    # Verifier si la colonne est valide
    if not colonne_valide(colonne):
        return "COLONNE_INVALIDE"

    # Placer le pion dans la colonne choisie
    if not placer_pion(grille, colonne, joueur):
        return "COLONNE_PLEINE"

    # Verifier si le joueur actuel a gagne
    if verifier_victoire(grille, joueur):

        partie["gagnant"] = joueur
        partie["terminee"] = True

        return "VICTOIRE"

    # Verifier si la grille est pleine
    if grille_pleine(grille):

        partie["terminee"] = True

        return "MATCH_NUL"

    # Passer au joueur suivant
    partie["joueur_actuel"] = changer_joueur(joueur)

    return "COUP_VALIDE"
