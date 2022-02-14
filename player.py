'''Module player.py :
    - module qui gère le rafraichissement des images, le déplacement et les collisions du joueur
'''

import pygame
import mob as mobfile
from time import sleep
import sys

class Player:

    '''Classe Mob
       Fonctions : - __init__ ()
                   - RefreshPlayerImg ()
                   - Jump()
                   - Move ()
                   - Animation ()
                   - TestCollision ()
                   - ShowCoins ()'''

    def __init__(self : object, path : str, img : pygame.image , position : dict, speed : dict,  default_speed : dict,  masse : int, default_anim_time : int, coins : int):

        '''init:
            construcetur de l'objet
            args : - self : object
                   - path : str
                   - img : pygame.image
                   - position : dict
                   - speed : dict
                   - default_speed : dict
                   - masse : int
                   - default_anim_time : int
                   - coins : int

                '''

        #Initialisation
        self.path = path
        self.img = img
        self.imgList = []
        self.anim_img = ["idle", "saut", "crouch", "marche_0", "marche_1", "marche_2"]
        self.position= position
        self.default_speed = default_speed
        self.speed = speed
        self.masse = masse
        self.default_anim_time = default_anim_time
        self.anim_time = default_anim_time
        self.coins = coins
        self.LevelCoins = coins
        self.life = 1

        self.finish = 0
        self.isrun = 0
        self.safeTime = 0
        self.isjump = 0
        self.anim_counter = 1
        self.isleft = 0
        self.iscrouch = 0
        self.iscol = 0
        self.isground = 0
        self.ishead = 0
        self.rect = pygame.Rect(self.position["X"], self.position["Y"], 65, 129)

        self.bdead = False

        self.RefreshPlayerImg()

    def RefreshPlayerImg(self : object):

        '''RefreshPlayerImg:
            - rafraichi les images du joueur pour que ce soit fluide
            - args : - self:object

        '''

        listTmp = ["_grand_", "_petit_"]
        for j in listTmp:
            for i in self.anim_img:
                if (j == listTmp[1] and i != "crouch") or j == listTmp[0]:
                    perso_img = pygame.image.load(self.path + "/" + self.img + j + i + ".png")
                    perso_img.convert_alpha()
                    self.imgList.append(perso_img)
        self.currentImg = self.imgList[0]

    def Jump(self : object):

        '''Jump:
            - permet au joueur de sauter
            - args : - self:object

        '''

        if self.isjump == 1:

            if self.speed["vertical"] < 0:
                F = ( 0.5 * self.masse * (self.speed["vertical"]**2) )
            else:
                F = -( 0.5 * self.masse * (self.speed["vertical"]**2) )
            self.position["Y"] += int(round(F))
            if self.speed["vertical"] >= -self.default_speed["vertical"]:
                self.speed["vertical"] -= 1
        else:

            F = ( 0.5 * self.masse * ((self.default_speed["vertical"] - self.speed["vertical"])**2) )
            self.position["Y"] += int(F)
            if self.speed["vertical"] > 0:
                self.speed["vertical"] -= 1

    def Move(self, x_change : int , Map : object, mob : list):

        '''Move :
            - Permet au joueur de se déplacer et s'occcuper de gérer les images du déplacement du joueur
            - args : - self : object
                     - x_change : int
                     - Map : object
                     - mob : list

        '''

        #Test si le joueur est tombé
        if self.position["Y"] >= 700:
            self.bdead = True
            self.LevelCoins = self.coins

        if ((self.isleft == 1 and Map.x == 0) or (self.isleft == 0 and self.position["X"] <= 300)) or (Map.x <= -len(Map.ListMap[0]) * 60 + 1160 and self.position["X"] >= 300):
            self.position["X"] += x_change
        else:
            Map.x -= x_change
            for i in mob:
                i.position["X"] -= x_change

        if Map.x > 0:
            Map.x = 0

        if self.position["X"] < 0:
            self.position["X"] = 0


    def Animation(self : object):
        '''Animation :
            - gère les animations des images du joueurs
            - args : - self:object

        '''

        animList = [[8, 9, 10], [3, 4, 5]]
        animList2 = [[6, 7], [0, 1]]


        if self.iscrouch == 1 and self.life == 2:
            self.currentImg = self.imgList[2]
        elif self.isjump == 1:
            self.currentImg = self.imgList[animList2[self.life - 1][1]]
        else:
            if self.isrun == 0:
                self.currentImg = self.imgList[animList2[self.life - 1][0]]
                self.anim_time = self.default_anim_time
            else:

                self.currentImg = self.imgList[animList[self.life - 1][self.anim_counter]]
                if self.anim_time == 0:
                    self.anim_time = self.default_anim_time
                    if self.anim_counter == 2:
                        self.anim_counter = 0
                    else:
                        self.anim_counter += 1
                else:
                    self.anim_time -= 1

    def TestCollision(self : object, App : object, CollisionList : list, x_change : int, old_y : int, Map : object, mob : list):

        '''TestCollision:
            -   Gère les collisions entre les mobs et le décors ainsi que les mobs et le joueur
            - args : - self:object
                     - App : object
                     - CollisionList : list
                     - x_change : int
                     - ols_y : int
                     - Map : object
                     - mob : list

        '''

        #Création des collisions autour du joueur
        if self.life == 2:
            self.rect = pygame.Rect(self.position["X"], self.position["Y"], 65, 129)
            groundRect = pygame.Rect(self.position["X"] + 12, self.position["Y"] + 127, 40, 15)
            headRect = pygame.Rect(self.position["X"] + 12, self.position["Y"] - 5, 40, 15)
            leftRect = pygame.Rect(self.position["X"] - 5, self.position["Y"] + 10, 15, 109)
            rightRect = pygame.Rect(self.position["X"] + 60, self.position["Y"] + 10, 15, 109)
        else:
            self.rect = pygame.Rect(self.position["X"] + 7, self.position["Y"] + 64, 50, 65)
            groundRect = pygame.Rect(self.position["X"] + 20, self.position["Y"] + 127, 30, 15)
            headRect = pygame.Rect(self.position["X"] + 20, self.position["Y"] + 59, 30, 15)
            leftRect = pygame.Rect(self.position["X"] + 2, self.position["Y"] + 80, 15, 60)
            rightRect = pygame.Rect(self.position["X"] + 60, self.position["Y"] + 80, 15, 60)


        self.isground = 0
        self.ishead = 0

        if self.safeTime != 0:
            self.safeTime -= 1

        #Test si le joueur entre en contact avec un mob
        for i in App.mob:

            if self.rect.colliderect(i.rect):
                if i.name == "Champignon":
                    if self.life < 2:
                        self.life += 1
                    App.mob.remove(i)
                elif i.name == "Goomba":
                    MobHeadRect = pygame.Rect(i.position["X"], i.position["Y"] - 5, 60, 15)
                    if groundRect.colliderect(MobHeadRect):
                        self.isjump = 1
                        self.speed["vertical"] = 25
                        App.mob.remove(i)
                    else:
                        if self.safeTime == 0 and self.life == 2:
                            self.life -= 1
                            self.safeTime = 150
                        elif self.safeTime == 0 and self.life == 1:
                            self.bdead = True
                            self.LevelCoins = self.coins



        #Test des collisions avec le niveau
        if self.rect.collidelist(CollisionList) != -1:

            for i in range(len(CollisionList)):

                if self.rect.colliderect(CollisionList[i]):



                    if (leftRect.colliderect(CollisionList[i]) and self.isleft == 1) or (rightRect.colliderect(CollisionList[i]) and self.isleft == 0):

                        if x_change != 0:
                            self.Move(-x_change, Map, mob)

                        bloc_i = int((CollisionList[i][0] - Map.x - 10) / 60)

                        if Map.ListMap[8][bloc_i] == 6:
                            self.finish = 1
                            self.coins = self.LevelCoins

                    if headRect.colliderect(CollisionList[i]):

                        bloc_i = int((CollisionList[i][0] - Map.x) / 60) #Détection Bloc au-dessus
                        bloc_y = int(CollisionList[i][1] / 60)

                        if Map.ListMap[bloc_y][bloc_i] == 2: #Si bloc == Suprise
                            self.LevelCoins += 1
                            Map.ListMap[bloc_y][bloc_i] = 5

                            champignon = mobfile.Mob("ImgMob", 2, "Champignon", {"X" : CollisionList[i][0], "Y" : CollisionList[i][1] - 65},  {"horizontal" : 1, "vertical" : 43}, {"horizontal" : 3, "vertical" : 43}, 0.02)
                            App.mob.append(champignon)

                        elif Map.ListMap[bloc_y][bloc_i] == 3 and self.life == 2:
                            Map.ListMap[bloc_y][bloc_i] = 0

                        self.isjump = 0
                        self.ishead = 1

                    if groundRect.colliderect(CollisionList[i]):
                        self.isground = 1
                        self.isjump = 0


            if self.isground == 1:

                self.speed["vertical"] = self.default_speed["vertical"]
                self.position["Y"] = old_y

            if self.ishead == 1:
                self.position["Y"] = old_y


    def ShowCoins(self : object, App : object, CoinsImg : pygame.image):

        '''init:
            - gère l'affichage des pièces sur la fenetre
            - args : - self:object
                     - App : object
                     - CoinsImg : pygame.image

        '''


        App.window_Surface.blit(CoinsImg, (5, 5))

        text = App.font.render(str(self.LevelCoins), True, (0, 0, 0))
        textRect = text.get_rect()

        textRect.center = (25,28)
        App.window_Surface.blit(text, textRect)



