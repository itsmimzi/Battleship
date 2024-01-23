"""
Auteurs     - Andre Pinel, Maryam Mouatadid
But         - Programmation d'un jeu de Bataille Navale avec implementation d'une IA.
Date        - Trimestre Automne 2023
Version     - BattleshipV2


Programme principal :

"""

import random


class Bateau:

    def __init__(self, taille):
        """ Constructeur de classe """
        self.ligne = random.randrange(0, 9)
        self.colonne = random.randrange(0, 9)
        self.taille = taille
        self.orientation = random.choice(["horizontal", "vertical"])
        self.indexes = self.genere_index()

    def genere_index(self):
        """
        Génère les index des cases occupées par un bateau en fonction de sa position, taille et orientation.

        Returns:
            Liste des index des cases occupées par le bateau.
        """

        # On calcule l'index de départ en convertissant la position (ligne, colonne) en un index unique sur la grille de taille 10x10
        indexDepart = self.ligne * 10 + self.colonne
        # Si le bateau est orienté horizontalement, génère les index en ajoutant i à l'index de départ pour chaque i allant de 0 à taille-1
        if self.orientation == "horizontal":
            return [indexDepart + i for i in range(self.taille)]
        # Si le bateau est orienté verticalement, génère les index en ajoutant i * 10 à l'index de départ pour chaque i allant de 0 à taille-1
        elif self.orientation == "vertical":
            return [indexDepart + i * 10 for i in range(self.taille)]


class Joueur:

    def __init__(self):
        """ Constructeur de classe """
        self.bateaux = []  # bateaux du joueur
        self.recherches = ["I" for i in
                           range(100)]  # tableau des emplacements : "I" pour inconnu, "T" pour Touché, "R" pour Raté
        self.placer_bateaux(
            tailles=[5, 4, 3, 3, 2])  # fonction qui assure que les bateaux sont dans les bonnes dimensions
        liste_des_listes = [bateau.indexes for bateau in self.bateaux]  # Liste des listes des indexes des bateaux
        self.indexes = [indice for liste in liste_des_listes for indice in liste]

    def placer_bateaux(self, tailles):
        """
        Place les bateaux sur la grille du jeu tout en respectant les limites et en évitant les collisions.

        Parameters:
            tailles (list): Liste des tailles des bateaux à placer.

        Returns:
            None
        """
        # Pour chaque taille de bateau spécifiée
        for taille in tailles:

            estPlace = False
            # Tant que le bateau n'est pas placé avec succès
            while not estPlace:
                bateau = Bateau(taille)  # creation d'un nouveau bateau
                positionEstValide = True  # verifier si la position choisie est possible

                # Vérifie chaque index du bateau
                for i in bateau.indexes:
                    # Vérifie que tous les indexes sont inférieurs à 100 (dans les limites de la grille)
                    if i >= 100:
                        positionEstValide = False
                        break

                    # Calcule la nouvelle ligne et colonne à partir de l'index
                    new_ligne = i // 10
                    new_colonne = i % 10

                    # Vérifie que la nouvelle position ne diffère pas de celle du bateau
                    if new_ligne != bateau.ligne and new_colonne != bateau.colonne:
                        positionEstValide = False
                        break

                    # Vérifie s'il y a une intersection avec un autre bateau déjà placé
                    for autreBateau in self.bateaux:
                        if i in autreBateau.indexes:
                            positionEstValide = False
                            break

                # Place le nouveau bateau s'il n'y a pas de collision
                if positionEstValide:
                    self.bateaux.append(bateau)
                    estPlace = True

    def afficher_bateaux(self):
        """
        Affiche les coordonnées des bateaux d'un joueur sur la grille.

        Returns:
            None
        """
        # Liste de symboles "-" pour les positions vides et "X" pour les positions occupées par un bateau
        indexes = ["-" if i not in self.indexes else "X" for i in range(100)]
        # Affiche la grille ligne par ligne
        for ligne in range(10):
            # Utilise " ".join pour afficher chaque ligne de la grille séparée par un espace
            print(" ".join(indexes[(ligne - 1) * 10:ligne * 10]))


class Jeu:

    def __init__(self, humain1, humain2):
        self.agentHumain1 = humain1
        self.agentHumain2 = humain2
        self.joueur1 = Joueur()  # joueur 1 de la partie
        self.joueur2 = Joueur()  # joueur2 de la partie
        self.tourJoueur1 = True  # variable booleenne qui indique le tour du joueur, elle peut etre en fonction d'un des 2 joueurs seulement.
        self.tourAI = True if not self.agentHumain1 else False  # variable booleenne qui indique le tour de l'ordinateur
        self.fin = False  # variable booléenne pour verifier la fin de la partie
        self.result = None  # Résultat du jeu/ de la partie

    def jouer_coup(self, i):
        """
        Fonction qui permet de jouer un coup en fonction de l'indice (index) spécifié.

        Parameters:
            i (int): Indice de l'emplacement visé sur la grille.

        Returns:
            None
        """

        # On commence par designer qui est le joueur courant et qui est son adversaire
        joueurCourant = self.joueur1 if self.tourJoueur1 else self.joueur2
        adversaire = self.joueur2 if self.tourJoueur1 else self.joueur1
        coup = False

        # On établit les etats de coups tel que "T" pour touché si le coup est réussi ; sinon "R" pour raté
        if i in adversaire.indexes:
            joueurCourant.recherches[i] = "T"
            coup = True
            # si le coup est réussi, on vérifie si le bateau est deja coulé ("C")
            for bateau in adversaire.bateaux:
                estCoule = True
                for i in bateau.indexes:
                    if joueurCourant.recherches[i] == "I":  # "I" désigne une position inconnue encore
                        estCoule = False
                        break
                if estCoule:
                    for i in bateau.indexes:
                        joueurCourant.recherches[i] = "C"
        else:
            joueurCourant.recherches[i] = "R"

        # On vérifie si la partie est terminée
        estGameOver = True

        for i in adversaire.indexes:
            if joueurCourant.recherches[i] == "I":
                estGameOver = False
        self.fin = estGameOver
        self.result = 1 if self.tourJoueur1 else 2

        # Changer le joueur courant (passer la main)
        if not coup:
            self.tourJoueur1 = not self.tourJoueur1

            # Interchanger le tour entre l'agent humain et l'IA
            if (self.agentHumain1 and not self.agentHumain2) or (not self.agentHumain1 and self.agentHumain2):
                self.tourAI = not self.tourAI

    def ia_aleatoire(self):
        """ Fonction qui implémente un premier agent intelligent à coups aléatoires.
            L'agent choisi aléatoirement les positions de ses coups dans la liste des indexes marqués "I" de son opposant. """

        # Si c'est le tour du joueur1, on récupere sa liste de recherches ; sinon celle du joueur2
        listeRecherches = self.joueur1.recherches if self.tourJoueur1 else self.joueur2.recherches

        # On obtient les indices des positions marquées "I" pour inconnu
        positionsInconnues = [i for i, caract in enumerate(listeRecherches) if caract == "I"]

        # Si des positions inconnues existent
        if len(positionsInconnues) > 0:
            # Choix aléatoire d'une position inconnue
            position_aleatoire = random.choice(positionsInconnues)
            # Joue un coup à la position choisie
            self.jouer_coup(position_aleatoire)

    def ia_intermediaire(self):
        """ Fonction qui implémente un agent intelligent avec calcul probabiliste des positions."""

        # On commence par récupérer la liste de recherches du joueur1
        # On obtient les indices des positions marquées "I" pour inconnu ; et les indices des positions "T" pour touché
        listeRecherches = self.joueur1.recherches if self.tourJoueur1 else self.joueur2.recherches
        positionsInconnues = [i for i, caract in enumerate(listeRecherches) if caract == "I"]
        positionsTouchees = [i for i, caract in enumerate(listeRecherches) if caract == "T"]

        # On inspecte les cases +1 adjacentes à une position "T"
        inconnuesAvecVoisinTouche = []
        # On inspecte les cases +1 adjacentes à 2 positions "T"
        inconnuesAvecVoisinTouche2 = []
        for indice in positionsInconnues:
            if (indice + 1 in positionsTouchees) or (indice - 1 in positionsTouchees) or (
                    indice - 10 in positionsTouchees) or (indice + 10 in positionsTouchees):
                inconnuesAvecVoisinTouche.append(indice)
            if (indice + 2 in positionsTouchees) or (indice + 2 in positionsTouchees) or (
                    indice - 20 in positionsTouchees) or (indice + 20 in positionsTouchees):
                inconnuesAvecVoisinTouche2.append(indice)

        # Choisir une case "I" avec un n-1 voisin "T" et un n-2 voisin "T" adjacents
        for indice in positionsInconnues:
            if indice in inconnuesAvecVoisinTouche and indice in inconnuesAvecVoisinTouche2:
                self.jouer_coup(indice)
                return

        # Sinon choisir une case "I" avec un n-1 voisin "T" seulement
        if len(inconnuesAvecVoisinTouche) > 0:
            self.jouer_coup(random.choice(inconnuesAvecVoisinTouche))
            return

        verifBoard = []
        for indice in positionsInconnues:
            ligne = indice // 10
            colonne = indice % 10
            if (ligne + colonne) % 2 == 0:
                verifBoard.append(indice)
        if len(verifBoard) > 0:
            self.jouer_coup(random.choice(verifBoard))
            return

        # Sinon choisir une case "I" aleatoire
        self.ia_aleatoire()


# joueur1 = Joueur()
# joueur1.afficher_bateaux()
