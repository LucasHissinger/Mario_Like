'''Module Mob.py :
    - module qui gère les objets et enemis du jeu ( rafraichissement, déplacement, création,...)
'''

import pygame

class Mob:
    '''Classe Mob
       Fonctions : - __init__ ()
                   - RefreshMobImg ()
                   - Move ()
                   - Animation ()
                   - TestCollision ()
                   - Gravity ()'''

    def __init__(self : object, path : str, nbImg : int, name : str, position : dict,  speed : dict, default_speed : dict, masse : int):
        '''init:
            - constructeur de l'objet
            - args : - self:object
                     - path : str
                     - nbImg : int
                     - name : str
                     - position : dict
                     - speed : dict
                     - default_speed : dict
                     - masse : int
        '''
        #Initialisation des variables
        self.time_alive = 0
        self.path = path
        self.currentImgNb = 0
        self.nbImg = nbImg
        self.name = name
        self.position = position
        self.default_speed = default_speed
        self.speed = speed
        self.masse = masse
        self.rect = pygame.Rect(self.position["X"], self.position["Y"], 60, 60)


        self.isleft = 1
        self.isground = 0
        self.imgList = []

        self.RefreshMobImg()

    def RefreshMobImg(self : object):
        '''RefreshMobImg:
            - rafraichi les images des mobs du jeu pour que ce soit fluide
            - args : - self:object

        '''

        for i in range(self.nbImg):
            mob_img = pygame.image.load(self.path + "/" + "Mob_" + self.name + "_" + str(i) + ".png")
            mob_img.convert_alpha()
            self.imgList.append(mob_img)
        self.currentImg = mob_img

    def Move(self : object, Map : object, App : object):
        '''Move:
            - s'occupe de gérer les déplacements des Mobs
            - args : - self:object
                     - Map : object
                     - App : object

        '''

        if self.position["X"] - Map.x <= 0:
            self.isleft = 0

        self.Animation()

        self.time_alive += 1

        if self.isleft == 0:
            self.position["X"] += self.speed["horizontal"]
        else:
            self.position["X"] -= self.speed["horizontal"]

    def Animation(self : object):

        '''Animation:
            - gère l'animation des mobs
            - args : - self:object

        '''

        #Test si le temps d'immunité est fini
        if int((self.time_alive-1) / 25) != int(self.time_alive / 25) :

            if self.currentImgNb == 0:

                self.currentImg = self.imgList[1]
                self.currentImgNb = 1
            else:
                self.currentImg = self.imgList[0]
                self.currentImgNb = 0

    def TestCollision(self, CollisionList : list, old_y : int , Map : object, player :object):

        '''TestCollision:
            -   Gère les collisions entre les mobs et le décors ainsi que les mobs et le joueur
            - args : - self:object
                     - CollisionList : list
                     - ols_y : int
                     - Map : object
                     - player : object

        '''

        self.rect = pygame.Rect(self.position["X"], self.position["Y"], 60, 60)
        self.isground = 0

        if self.rect.collidelist(CollisionList) != -1:

            for i in range(len(CollisionList)):

                if self.rect.colliderect(CollisionList[i]):

                    groundRect = pygame.Rect(self.position["X"] + 10, self.position["Y"] + 52, 40, 15)
                    leftRect = pygame.Rect(self.position["X"] - 5, self.position["Y"] + 5, 10, 50)
                    rightRect = pygame.Rect(self.position["X"] + 55, self.position["Y"] + 5, 10, 50)

                    if (leftRect.colliderect(CollisionList[i]) and self.isleft == 1):

                        self.position["X"] += self.speed["horizontal"]
                        self.isleft = 0

                    if (rightRect.colliderect(CollisionList[i]) and self.isleft == 0):

                        self.position["X"] -= self.speed["horizontal"]
                        self.isleft = 1

                    if groundRect.colliderect(CollisionList[i]):
                        self.isground = 1


            if self.isground == 1:

                self.speed["vertical"] = self.default_speed["vertical"]
                self.position["Y"] = old_y

    def Gravity(self : object):
        '''Gravity:
            - S'occupe d'appliquer la gravité terrestre aux Mobs
            - args : - self:object

        '''
        #Calcul de la force subit par le mob
        F = ( 0.5 * self.masse * ((self.default_speed["vertical"] - self.speed["vertical"])**2) )
        self.position["Y"] += int(F)
        if self.speed["vertical"] > 0:
            self.speed["vertical"] -= 1


