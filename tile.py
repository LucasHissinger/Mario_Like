'''Module tile.py :
    - Contient la class Map
'''

import pygame
import mob as mobfile

class Map:
    '''Map :
        - classe de création principal du niveau
        - fonctions : - __init__()
                      - DesignLevel()
                      - RefreshMob()
    '''

    def __init__(self:object, x:int, ListMap:list):
        '''__init__ :
            - constructeur de l'objet Map
            - args : - self:object
                     - x:int
                     - ListMap:list
        '''

        self.x = x
        self.ListMap = ListMap

    def DesignLevel(self:object, surface:pygame.Surface, grass:pygame.image, surprise:pygame.image, brick:pygame.image, flower:pygame.image, bloc_use:pygame.image, end:pygame.image):
        '''DesignLevel : 
            - Créer le niveau en cours
            - args : - self:object
                     - surface:pygame.Surface
                     - grass:pygame.image
                     - surprise:pygame.image
                     - brick:pygame.image
                     - flower:pygame.image
                     - bloc_use:pygame.image
                     - end:pygame.image
            - return : - collision
        '''

        #Affichage du niveau
        collision = []
        for j, ligne in enumerate(self.ListMap):
            for i, colonne in enumerate(ligne):
                if colonne == 1:
                    surface.blit(grass, (i*60 + self.x, j*60))
                    collision.append(pygame.Rect(i*60 + self.x, j*60, 60, 60))
                elif colonne == 2:
                    surface.blit(surprise, (i*60 + self.x, j*60))
                    collision.append(pygame.Rect(i*60 + self.x, j*60, 60, 60))
                elif colonne == 3:
                    surface.blit(brick, (i*60 + self.x, j*60))
                    collision.append(pygame.Rect(i*60 + self.x, j*60, 60, 60))
                elif colonne == 4:
                    surface.blit(flower, (i*60 + self.x, (j+1)*60 - 40))
                elif colonne == 5:
                    surface.blit(bloc_use, (i*60 + self.x, j*60))
                    collision.append(pygame.Rect(i*60 + self.x, j*60, 60, 60))
                elif colonne == 6:
                    surface.blit(end, (i*60 + self.x, j+100))
                    collision.append(pygame.Rect(i*60 + self.x, j*60, 130, 60))
                    collision.append(pygame.Rect(i*60 + 40 + self.x, 50, 20, 800))

        return collision

    def RefreshMob(self:object, App:object):
        '''RefreshMob :
            - Créer les mobs du niveau en cours
            - args : - self:object
                     - App:object
        '''
        #Affichage des mobs
        for j, ligne in enumerate(self.ListMap):
            for i, colonne in enumerate(ligne):
                if colonne == 7:
                        goomba = mobfile.Mob("ImgMob", 2, "Goomba", {"X" : i*60, "Y" : j*60},  {"horizontal" : 1, "vertical" : 43}, {"horizontal" : 3, "vertical" : 43}, 0.02)
                        App.mob.append(goomba)

