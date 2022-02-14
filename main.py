'''Module main.py :
    - module principal
'''

import pygame
import player
import mob
import sys
import tile
import levels
import os
from pickle import dump,load
from time import sleep

pygame.init()

class App:
    '''App :
        - classe principale
        - fonctions : - __init__()
                      - Main()
                      - ShowButton()
                      - RefreshSplashScreen()
                      - RefreshLevelSreen()
                      - RefreshMob()
                      - Refresh()
                      - DeadScreen()
                      - WinScreen()
                      - Save()
                      - Load()
    '''

    def __init__(self:object, iNbLevel:int):
        '''__init__ :
            - constructeur de l'objet App
            - args : - self:object
                     - iNbLevel:int
        '''


        #Create pygame display
        pygame.display.set_caption("Mario")
        self.font = pygame.font.Font('freesansbold.ttf', 25)

        self.window_Surface = pygame.display.set_mode((1150, 600), pygame.HWSURFACE)
        self.window_Surface.fill((255, 255, 255))

        self.iUnlockLevel = 1
        self.iCurrentLevel = 0

        self.mob = []

        self.bSplashScreen = True
        self.bLevelScreen = False
        self.lLevelRect = []
        self.iNbLevel = iNbLevel
        for i in range(self.iNbLevel // 5 + 1):
            if (self.iNbLevel - i*5) >= 5:
                iColonne = 5
            else:
                iColonne = self.iNbLevel % 5
            for j in range(iColonne):
                self.lLevelRect.append(pygame.Rect(350 + j*90, 80 + i * 90, 61, 61))

        self.AnimTime = 8  
        self.step = [12, 12]
        self.Map = tile.Map(0, [])
        self.RefreshMob()

    def Main(self:object, x_change:int, y_change:int):
        '''Main :
            - fonction principal
            - Gère les différents affichages d'écran
            - args : - self:object
                     - x_change:int
                     - y_change:int
            - return : - x_change
                       - y_change
        ''' 
        

        if App.bSplashScreen: #Ecran de démarrage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if QuitImgRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.display.quit()
                        sys.exit()
                    
                    if NewImgRect.collidepoint(pygame.mouse.get_pos()):
                        App.bSplashScreen = False
                        App.bLevelScreen = True
                        self.iUnlockLevel = 1
                        Mario.coins, Mario.LevelCoins = 0, 0
                    
                    if ContinueImgRect.collidepoint(pygame.mouse.get_pos()):
                        App.bSplashScreen = False
                        App.bLevelScreen = True


            y_change = App.RefreshSplashScreen(y_change)
            return x_change, y_change

        if App.bLevelScreen: #Ecran des niveaux

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(App.iUnlockLevel):
                        if App.lLevelRect[i].collidepoint(pygame.mouse.get_pos()):
                            App.bLevelScreen = False
                            Mario.position = {"X" : 200, "Y" : 270}
                            x_change, Mario.isrun, self.Map.x = (0 for _ in range(3))
                            self.Map.x, self.Map.ListMap = 0, levels.GetLevels()[i]
                            self.mob = []
                            self.RefreshMob()
                            self.Map.RefreshMob(App)
                            self.iCurrentLevel = i

            App.RefreshLevelSreen()
            return x_change, y_change
                    

        if not Mario.bdead and not Mario.finish: #Ecran de jeu

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()


                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]: #Player Crouch
                    if Mario.life == 2:
                        Mario.iscrouch = 1
                        Mario.isrun = 0
                        x_change = 0

                elif keys[pygame.K_RIGHT]: #Player Right
                    x_change = Mario.speed["horizontal"]
                    Mario.isrun = 1
                    Mario.isleft = 0

                elif keys[pygame.K_LEFT]: #Player Left

                    x_change = -Mario.speed["horizontal"]
                    Mario.isrun = 1
                    Mario.isleft = 1



                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: #Player Jump
                        if Mario.isjump == 0:
                            Mario.speed["vertical"] = Mario.default_speed["vertical"]
                        Mario.isjump = 1

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN: #Player Stop Crouching
                        Mario.iscrouch = 0

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT: #Player Stop Running
                        x_change = 0
                        Mario.isrun = 0

            App.Refresh(x_change,)
            return x_change, y_change

        if Mario.bdead: #Ecran de mort
            rButton = pygame.Rect(780, 500, 348, 55)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    Mario.bdead = False
                    Mario.position = {"X" : 200, "Y" : 270}

                    x_change, Mario.isrun, self.Map.x = (0 for _ in range(3))
                    Mario.life = 1
                    self.mob = []
                    self.Map.RefreshMob(self)
                    self.Map.ListMap = levels.GetLevels()[self.iCurrentLevel]
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if rButton.collidepoint(pygame.mouse.get_pos()):
                        Mario.bdead = False
                        Mario.position = {"X" : 200, "Y" : 270}

                        x_change, Mario.isrun, self.Map.x = (0 for _ in range(3))
                        Mario.life = 1
                        
                        self.bSplashScreen = True
                
            App.DeadScreen(rButton)
            return x_change, y_change
            
        if Mario.finish: #Ecran de victoire      
            if self.iCurrentLevel + 1 == self.iUnlockLevel:
                self.iUnlockLevel += 1
            x_change = 0
            App.WinScreen()

            return x_change, y_change

    def ShowButton(self:object, New:list, Continue:list, Quit:list):
        '''ShowButton :
            - Affiche les Buttons du SplashScreen
            - args : - self:object
                     - New:list
                     - Continue:list
                     - Quit:list
        '''

        self.window_Surface.blit(New[0], New[1])
        self.window_Surface.blit(Continue[0], Continue[1])
        self.window_Surface.blit(Quit[0], Quit[1])

    def RefreshSplashScreen(self:object, y_change:int):
        '''RefreshSplashScreen :
            - Met à jour le SplashScreen
            - args : - self:object
                     - y_change:int
            - return : - y_change
        '''

        self.window_Surface.blit(MenuBGSplashImg, (0, 0))

        
        #Test si la souris est sur les Bouttons
        if NewImgRect.collidepoint(pygame.mouse.get_pos()):
            self.ShowButton([NewImgScale, (350, 300 + y_change)], [ContinueImg, (350, 380 + y_change)], [QuitImg, (350, 460 + y_change)])
        
        elif ContinueImgRect.collidepoint(pygame.mouse.get_pos()):
            self.ShowButton([NewImg, (350, 300 + y_change)], [ContinueImgScale, (350, 380 + y_change)], [QuitImg, (350, 460 + y_change)])

        elif QuitImgRect.collidepoint(pygame.mouse.get_pos()):
            self.ShowButton([NewImg, (350, 300 + y_change)], [ContinueImg, (350, 380 + y_change)], [QuitImgScale, (350, 460 + y_change)])

        else:
            self.ShowButton([NewImg, (350, 300 + y_change)], [ContinueImg, (350, 380 + y_change)], [QuitImg, (350, 460 + y_change)])

        #Animation des Bouttons
        if y_change == self.AnimTime:
            self.AnimTime = -self.AnimTime
        
        if self.step[0] == 0:
            if self.AnimTime > 0:
                y_change += 1
            else:
                y_change -= 1
            self.step[0] = self.step[1]
        else:
            self.step[0] -= 1
        

        pygame.display.flip() #Refresh Display
        
        sleep(0.001)

        return y_change

    def RefreshLevelSreen(self:object):
        '''RefreshLevelScreen :
            - Met à jour l'écran des Niveaux
            - args : -self:object
        '''

        self.window_Surface.blit(MenuBGLevelImg, (0, 0))

        #Test si la souris passe sur un niveau
        for i in range(len(self.lLevelRect)):
            if self.lLevelRect[i].collidepoint(pygame.mouse.get_pos()):
                iLevelSelect = i + 1
                break 
            else:
                iLevelSelect = 0

        #Affiche Les niveaux
        for i in range(self.iNbLevel // 5 + 1):

            if (self.iNbLevel - i*5) >= 5:
                colonne = 5
            else:
                colonne = self.iNbLevel % 5
            for j in range(colonne):

                self.window_Surface.blit(LevelCaseImg, (350 + j*90, 80 + i * 90))
                if self.iUnlockLevel >= i*5 + j + 1:
                    if iLevelSelect == i*5 + j + 1:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)

                    NumberText = self.font.render(str(i*5 + j + 1), True, color) 
                    textRect = NumberText.get_rect()

                    textRect.center = (380 + j*90, 110 + i * 90)
                    App.window_Surface.blit(NumberText, textRect)
                else:
                    App.window_Surface.blit(LevelCrossImg, (350 + j*90, 80 + i * 90))

        pygame.display.flip() #Refresh Display
        
        sleep(0.005)
        
    def RefreshMob(self:object):
        '''RefreshMob :
            - Met à jour les mobs de la liste mob
            - args : - self:object
            - return : - mob_old_y
        '''

        mob_old_y = []

        for i in self.mob:
            mob_old_y.append(i.position["Y"])
            i.Gravity()     
            i.Move(self.Map, self)
        
        return mob_old_y

    def Refresh(self:object, x_change:int):        
        '''Refresh :
            - Met à jour l'écran principal du jeu : l'écran de jeu
            - args : - self:object
                     - x_change:int
        '''

        mario_old_y = Mario.position["Y"] #Récupère l'ancienne position y du Mario 
        Mario.Jump()
        Mario.Move(x_change, self.Map, self.mob)
       

        Mario.Animation()

        if Mario.isleft == 1:
            Mario.currentImg = pygame.transform.flip(Mario.currentImg, True, False) #Met à jour la direction du Mario



        self.window_Surface.blit(BGImg,(0, 0))

        Mario.ShowCoins(self, CoinsImg)



        CollisionList = self.Map.DesignLevel(self.window_Surface, GrassImg, BlocSurpriseImg, BrickImg, FlowerImg, BlocUseImg, EndImg) #Récupère les collision du niveaux et le met à jour

        Mario.TestCollision(App, CollisionList, x_change, mario_old_y, self.Map, self.mob)

        mob_old_y = self.RefreshMob()

        for j, i in enumerate(self.mob):
            i.TestCollision(CollisionList, mob_old_y[j], self.Map, Mario)
            self.window_Surface.blit(i.currentImg,(i.position["X"], i.position["Y"])) #Refresh Mob
        

        self.window_Surface.blit(Mario.currentImg,(Mario.position["X"], Mario.position["Y"])) #Refresh Mario            

        pygame.display.flip() #Refresh Display
        
        sleep(0.005)
    
    def DeadScreen(self:object, rButton:pygame.Rect):
        '''DeadScreen :
            - Met à jour l'écran de mort 
            - args : - self:object
                     - rButton:pygame.Rect
        '''


        self.window_Surface.blit(MenuBGLevelImg, (0, 0))

        self.window_Surface.blit(GameOverImg, (0, 0))

        #Test si la souris passe su le Boutton Principal
        if rButton.collidepoint(pygame.mouse.get_pos()):
            self.window_Surface.blit(ButtonPrincipalScaleImg, (780, 500))
        else: 
            self.window_Surface.blit(ButtonPrincipalImg, (780, 500))

        pygame.display.flip() #Refresh Display
        
        sleep(0.005)
    
    def WinScreen(self:object):
        '''WinScreen :
            - Met à jour l'écran de victoire du niveau
            - args : - self:object
        '''

        self.Save() #Sauvegarde les scores 

        self.window_Surface.blit(MenuBGLevelImg, (0, 0))

        self.window_Surface.blit(WinImg, (0, 0))

        pygame.display.flip() #Refresh Display
        
        sleep(3)

        self.bLevelScreen = True
        Mario.finish = False
    
    def Save(self:object):
        '''Save :
            - Sauvegarde les scores dans le fichier Score.txt
            - args : - self:object
        '''

        file = open("Score.txt",'wb')
        dump([self.iUnlockLevel, Mario.coins],file)
        file.close()
    
    def Load(self:object):
        '''Load :
            -Récupère les scores sauvegardés dans le fichier Score.txt
            - args : - self:object
        '''

        file = open("Score.txt",'rb')
        if os.stat("Score.txt").st_size > 2:
            lfile = load(file)
            self.iUnlockLevel, Mario.coins, Mario.LevelCoins = lfile[0], lfile[1], lfile[1]
        file.close()


#Init var
x_change = 0
y_change = 0

lLevels = levels.GetLevels() #Récupération des niveaux

#Création des objets App et Player
App = App(len(lLevels))
Mario = player.Player("ImgMario", "mario", {"X" : 200, "Y" : 270}, {"horizontal" : 3, "vertical" : 43}, {"horizontal" : 3, "vertical" : 43}, 0.02, 12, 0)

App.Load() #Récupération des Scores

#Initialisation des Images
MenuBGSplashImg = pygame.image.load("ImgSplashScreen/MarioMenuBGSplash.png").convert_alpha()
MenuBGLevelImg = pygame.image.load("ImgSplashScreen/MarioMenuBGLevel.png").convert_alpha()

NewImg = pygame.image.load("ImgSplashScreen/MenuNew.png").convert_alpha()
NewImgScale = pygame.image.load("ImgSplashScreen/MenuNewScale.png").convert_alpha()
NewImgRect = pygame.Rect(350, 300 + y_change, NewImg.get_width(), NewImg.get_height())

ContinueImg = pygame.image.load("ImgSplashScreen/MenuContinue.png").convert_alpha()
ContinueImgScale = pygame.image.load("ImgSplashScreen/MenuContinueScale.png").convert_alpha()
ContinueImgRect = pygame.Rect(350, 380 + y_change, ContinueImg.get_width(), ContinueImg.get_height())

QuitImg = pygame.image.load("ImgSplashScreen/MenuQuit.png").convert_alpha()
QuitImgScale = pygame.image.load("ImgSplashScreen/MenuQuitScale.png").convert_alpha()
QuitImgRect = pygame.Rect(350, 460 + y_change, QuitImg.get_width(), QuitImg.get_height())

LevelCaseImg = pygame.image.load("ImgSplashScreen/LevelCase.png").convert_alpha()
LevelCrossImg = pygame.image.load("ImgSplashScreen/Cross.png").convert_alpha()

CoinsImg = pygame.image.load("ImgMario/Coins.png").convert_alpha()
BlocSurpriseImg = pygame.image.load("ImgTile/Bloc_surprise.png").convert_alpha()
BlocUseImg = pygame.image.load("ImgTile/Bloc_Worn.png").convert_alpha()
GrassImg = pygame.image.load("ImgTile/Bloc_Grass.png").convert_alpha()
BrickImg = pygame.image.load("ImgTile/Bloc_Brick.png").convert_alpha()
FlowerImg = pygame.image.load("ImgTile/Flower.png").convert_alpha()
EndImg = pygame.image.load("ImgTile/End.png").convert_alpha()

BGImg = pygame.image.load("ImgBG/GameBG.png").convert()

GameOverImg = pygame.image.load("ImgBG/GameOver.png").convert_alpha()
ButtonPrincipalImg = pygame.image.load("ImgBG/Button.png").convert_alpha()
ButtonPrincipalScaleImg = pygame.image.load("ImgBG/ButtonScale.png").convert_alpha()

WinImg = pygame.image.load("ImgBG/Win.png").convert_alpha()

#Boucle principal
while True:
    x_change, y_change = App.Main(x_change, y_change)