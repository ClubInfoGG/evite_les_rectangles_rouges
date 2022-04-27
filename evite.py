import pygame
import sys
import random
from pygame.locals import *

#commentaire

pygame.init()
pygame.font.init()

ECRAN_X = 400
ECRAN_Y = 400
ECRAN = pygame.display.set_mode((ECRAN_X, ECRAN_Y))
FPS = pygame.time.Clock()

BLANC = pygame.Color(255, 255, 255)
BLEU = pygame.Color(0, 0, 255)
ROUGE = pygame.Color(255, 0, 0)
NOIR = pygame.Color(0, 0, 0)

RECT_LARGEUR = 80
RECT_HAUTEUR = 25

POLICE_SYSTEME = pygame.font.SysFont('monospace', 24, True)

def rect_contour_centre(couleur, rectangle):
    x, y, l, h = rectangle
    pygame.draw.rect(ECRAN, NOIR, (x-l/2-1, y-h/2-1, l+2, h+2))
    pygame.draw.rect(ECRAN, couleur, (x-l/2, y-h/2, l, h))

def affiche_texte(message, couleur, police, position):
    ECRAN.blit(police.render(message, True, couleur), position)

def collision_rectangles_centre(rectangle_1, rectangle_2):
    x1, y1, l1, h1 = rectangle_1
    x2, y2, l2, h2 = rectangle_2
    l = (l1 + l2) / 2
    h = (h1 + h2) / 2

    if (x1 + l > x2 and x1 - l < x2) and (y1 + h > y2 and y1 - h < y2):
        return True
    return False


scene = "jeu"

x = ECRAN_X/2
y = ECRAN_Y/2
points = 0

ennemi_x = [ECRAN_X*3/3, ECRAN_X*5/3, ECRAN_X*7/3]
ennemi_y = [30, 70, 240]

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == MOUSEMOTION:
            if scene == 'jeu':
                x, y = event.__getattribute__('pos')
        elif event.type == MOUSEBUTTONDOWN:
            if scene == 'perdu':
                scene = 'jeu'
                points = 0
                ennemi_x = [ECRAN_X*3/3, ECRAN_X*5/3, ECRAN_X*7/3]
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    if scene == 'jeu':
        ECRAN.fill(BLANC)
        
        rect_contour_centre(BLEU, (x, y, RECT_LARGEUR, RECT_HAUTEUR))
        for i in range(len(ennemi_x)):
            ennemi_x[i] -= 1 + points/1000
            if ennemi_x[i] < -ECRAN_X/2:
                ennemi_x[i] += 2*ECRAN_X
                ennemi_y[i] = random.randrange(0, ECRAN_Y)
            if collision_rectangles_centre(
            (x, y, RECT_LARGEUR, RECT_HAUTEUR), 
            (ennemi_x[i], ennemi_y[i], RECT_LARGEUR, RECT_HAUTEUR)):
                scene = 'perdu'
            rect_contour_centre(ROUGE, (ennemi_x[i], ennemi_y[i], RECT_LARGEUR, RECT_HAUTEUR))

        points = points + 1
        str_points = str(points) + ' pts'
        decalage_gauche, rien = POLICE_SYSTEME.size(str_points)
        affiche_texte(str_points, NOIR, POLICE_SYSTEME, (ECRAN_X-10-decalage_gauche, 10))

    elif scene == 'perdu':
        ECRAN.fill(NOIR)
        affiche_texte('VOUS AVEZ PERDU', BLANC, POLICE_SYSTEME, (10, 10))
        affiche_texte('Score final: ' + str(points) + ' pts', ROUGE, POLICE_SYSTEME, (10, 50))
        affiche_texte('Cliquez pour rejouer', ROUGE, POLICE_SYSTEME, (10, 90))

    pygame.display.update()
    FPS.tick(60)