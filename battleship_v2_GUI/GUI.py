"""
Auteurs     - Andre Pinel, Maryam Mouatadid
But         - Programmation d'un jeu de Bataille Navale avec implementation d'une IA.
Date        - Trimestre Automne 2023
Version     - BattleshipV2


Programme principal :

"""

import pygame
from program import Joueur
from program import Jeu

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
pygame.display.set_caption("Battleship_v2")

police = pygame.font.SysFont("Comic Sans MS", 50)   # police du texte à afficher.

# Trois fichiers audios chargés pour les effets sonores.
sonTouche = pygame.mixer.Sound("touche.wav")
sonRate = pygame.mixer.Sound("rate.wav")
sonFin = pygame.mixer.Sound("finJeu.wav")

# Variables Globales de dimensionnement
taillecarre = 35                                # taille en pixels des cases dans la grille
margeHorz = taillecarre * 4                     # marge horizontale entre les bords de la fenêtre et la grille de jeu
margeVert = taillecarre                         #
WIDTH = taillecarre * 10 * 2 + margeHorz        #
HEIGHT = taillecarre * 10 * 2 + margeVert       #
MARGE = 10
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

#variables booléennes qui décident quels types d'agents participeront à la partie
agentHumain1 = True
agentHumain2 = False

GREY = (65,65,65)
WHITE = (230,230,230)
BLUE = (152,245,255)
GREEN = (50, 200, 150)
ORANGE = (250, 140, 20)
RED = (250, 50, 100)
SHIP = (102,205,170)
ETATS = {"I": GREY, "R": BLUE, "T": ORANGE, "C": RED}


def dessine_grilles(joueur, gauche=0, haut=0, search=False):
    """Fonction qui dessine la grille de jeu et/ou de recherche"""
    for i in range(100):
        x = gauche + i % 10 * taillecarre
        y = haut + i // 10 * taillecarre
        carre = pygame.Rect(x, y, taillecarre, taillecarre)
        pygame.draw.rect(SCREEN, WHITE, carre, width=3)
        if search:
            x += taillecarre // 2
            y += taillecarre // 2
            pygame.draw.circle(SCREEN, ETATS[joueur.recherches[i]], (x, y), radius=taillecarre // 4)


def dessiner_bateaux(joueur, gauche=0, haut=0):
    """Fonction qui dessine les bateaux dans la grille de jeu"""
    for bateau in joueur.bateaux:
        # coordonnée haute gauche du bateau
        x = gauche + bateau.colonne * taillecarre + MARGE
        y = haut + bateau.ligne * taillecarre + MARGE
        if bateau.orientation == "horizontal":
            largeur = bateau.taille * taillecarre - 2 * MARGE
            hauteur = taillecarre - 2 * MARGE
        else:
            largeur = taillecarre - 2 * MARGE
            hauteur = bateau.taille * taillecarre - 2 * MARGE
        # dessin d'un bateau utilisant une forme rectangle
        rectangle = pygame.Rect(x, y, largeur, hauteur)
        pygame.draw.rect(SCREEN, SHIP, rectangle, border_radius=15)



# MAIN
jeu = Jeu(agentHumain1, agentHumain2)


animation = True
pause = False
while animation:

    # GESTION DES EVENTS UTILISATEURS
    for event in pygame.event.get():

        # SOURIS
        # Si l'utilisateur ferme la fenêtre d'animation
        if event.type == pygame.QUIT:
            animation = False

        # Si l'utilisateur clique une fois :
        if event.type == pygame.MOUSEBUTTONDOWN and not jeu.fin:
            x,y = pygame.mouse.get_pos()
            # tour du 1er joueur
            if jeu.tourJoueur1 and (x < taillecarre*10) and (y < taillecarre*10): # (on verifie que le joueur joue son coup dans la case de recherche adverse)
                ligne = y // taillecarre
                colonne = x // taillecarre
                index = ligne*10 + colonne
                jeu.jouer_coup(index)
                if jeu.tourJoueur1:
                    sonTouche.play()  # Joue le son de touche pour le joueur 1
                else:
                    sonRate.play()  # Joue le son d'eau pour le joueur 2

            # tour du 2nd joueur
            elif not jeu.tourJoueur1 and (x > WIDTH - taillecarre*10) and (y > taillecarre*10 + margeVert): # (on verifie que le joueur2 joue son coup dans la case de recherche adverse)
                ligne = (y - taillecarre*10 - margeVert) // taillecarre
                colonne = (x - taillecarre*10 - margeHorz) // taillecarre
                index = ligne*10 + colonne
                jeu.jouer_coup(index)
                if not jeu.tourJoueur1:
                    sonTouche.play()  # Joue le son de touche pour le joueur 1
                else:
                    sonRate.play()  # Joue le son d'eau pour le joueur 2

        # CLAVIER :
        if event.type == pygame.KEYDOWN:
            # la touche ESC quitte l'animation
            if event.key == pygame.K_ESCAPE:
                animation = False
            # et la barre d'espace pause/reprend l'animation
            if event.key == pygame.K_SPACE:
                pause = not pause
            # touche ENTRER pour redémarrer une partie
            if event.key == pygame.K_RETURN:
                jeu = Jeu(agentHumain1, agentHumain2)

    #  EXECUTION
    if not pause:
        # dessine l'arrière-plan
        SCREEN.fill(GREY)

        # dessine les grilles de recherche des bateaux
        dessine_grilles(jeu.joueur1, search=True)  # dessine la grille de recherche du joueur 1, en haut à gauche
        dessine_grilles(jeu.joueur2, gauche=((WIDTH - margeHorz) // 2 + margeHorz), haut=((HEIGHT - margeVert)//2 + margeVert), search=True,)  # dessine la grille de recherche du joueur 2, en haut à droite

        # dessine les grilles de jeu des bateaux
        dessine_grilles(jeu.joueur1, haut=((HEIGHT - margeVert) // 2 + margeVert))  # dessine la grille de jeu du joueur 1, en bas à gauche
        dessine_grilles(jeu.joueur2, gauche=((WIDTH - margeHorz) // 2 + margeHorz))  # dessine la grille de jeu du joueur 2, en bas à droite

        # dessine les bateaux dans la grille de jeu
        dessiner_bateaux(jeu.joueur1, haut=(HEIGHT - margeVert) // 2 + margeVert)
        #dessiner_bateaux(jeu.joueur2, gauche=(HEIGHT - margeVert) // 2 + margeHorz)

        # Coups IA
        if not jeu.fin and jeu.tourAI:
             if jeu.tourJoueur1 :
                jeu.ia_intermediaire()
             else:
                jeu.ia_intermediaire()

        # Affiche le message de fin partie
        if jeu.fin:
            sonFin.play()
            message = "joueur " + str(jeu.result) + " a gagné !"
            textbox = police.render(message, False, GREY, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 - 240, HEIGHT//2 - 50))

        # met à jour l'affichage
        pygame.time.wait(100)
        pygame.display.flip()
