### Programme : Interface.py

##########                   IMPORTS                   ##########
import io, os, sys, picamera

import RPi.GPIO as GPIO

import pygame
from pygame.locals import *

import time

import warnings
#################################################################



warnings.filterwarnings('default', category=DeprecationWarning) #Affiche une alerte si une fonction depreciee est utilisee 
GPIO.setwarnings(False)                                         #On masque les avertissements GPIO



##########            INITIALISATION GPIO             ##########

GPIO.setmode(GPIO.BOARD)          #On va appeler les entrées GPIO par leur numéro sur la board
        
GPIO.setup([13,15,16,18,29,31,36,38],GPIO.OUT)    #On initialise les ports GPIO en sortie :

#On définit chaque sortie comme une sortie PWN, avec une fréquence de 10000Hz :
M1A = GPIO.PWM(16,10000)
M1B = GPIO.PWM(18,10000)
M2A = GPIO.PWM(13,10000)
M2B = GPIO.PWM(15,10000)
M3A = GPIO.PWM(36,10000)
M3B = GPIO.PWM(38,10000)
M4A = GPIO.PWM(29,10000)
M4B = GPIO.PWM(31,10000)

ListeSorties = [M1A,M1B,M2A,M2B,M3A,M3B,M4A,M4B]

#On initialise toutes les sorties à 0
M1A.start(0)
M1B.start(0)
M2A.start(0)
M2B.start(0)
M3A.start(0)
M3B.start(0)
M4A.start(0)
M4B.start(0)

#################################################################



##########       INITIALISATION PYGAME ET CAMERA       ##########

pygame.init()                                   #On initialise PyGame
res = pygame.display.list_modes()               #On récupère la taille de l'écran
fenêtre = pygame.display.set_mode(res[0])     #On ouvre une fenêtre de la taille de l'écran
pygame.display.toggle_fullscreen()              #On se met en plein écran
pygame.mouse.set_visible = False                #On cache la souris

camera = picamera.PiCamera(sensor_mode=1)                    #On crée un objet caméra, qui filme en 1080p
filme = False

#################################################################


##########              FONCTIONS MOTEURS              ##########

def ArretTotal() :
    """Fonction stoppant tous les moteurs"""
    for sortie in ListeSorties :            #Pour chaque sortie GPIO
        sortie.ChangeDutyCycle(0)               #On la met à 0


def Avancer(vitesse) :
    """Fonction programmant les moteurs pour que le sous marin avance à la vitesse donnée en argument (en %)"""
    if vitesse >= 0 and vitesse <= 100 :    #La vitesse doit être comprise entre 0 et 100
        M1A.ChangeDutyCycle(vitesse)        #Les deux moteurs horizontaux "avancent"
        M2A.ChangeDutyCycle(vitesse)
        M1B.ChangeDutyCycle(0)
        M2B.ChangeDutyCycle(0)

def Reculer(vitesse) :
    """Fonction programmant les moteurs pour que le sous marin recule à la vitesse donnée en argument (en %)"""
    if vitesse >= 0 and vitesse <= 100 :
        M1B.ChangeDutyCycle(vitesse)        #Les deux moteurs horizontaux "reculent"
        M2B.ChangeDutyCycle(vitesse)
        M1A.ChangeDutyCycle(0)
        M2A.ChangeDutyCycle(0)

def Monter(vitesse) :
    """Fonction programmant les moteurs pour que le sous marin monte à la vitesse donnée en argument (en %)"""
    if vitesse >= 0 and vitesse <= 100 :
        M3A.ChangeDutyCycle(vitesse)        #Les deux moteurs verticaux "avancent"
        M4A.ChangeDutyCycle(vitesse)
        M3B.ChangeDutyCycle(0)
        M4B.ChangeDutyCycle(0)

def Descendre(vitesse) :
    """Fonction programmant les moteurs pour que le sous marin descende à la vitesse donnée en argument (en %)"""
    if vitesse >= 0 and vitesse <= 100 :
        M3B.ChangeDutyCycle(vitesse)        #Les deux moteurs verticaux "reculent"
        M4B.ChangeDutyCycle(vitesse)
        M3A.ChangeDutyCycle(0)
        M4A.ChangeDutyCycle(0)

def StopHorizontal():
    M1A.ChangeDutyCycle(0)
    M1B.ChangeDutyCycle(0)
    M2A.ChangeDutyCycle(0)
    M2B.ChangeDutyCycle(0)

def StopVertical():
    M3A.ChangeDutyCycle(0)
    M3B.ChangeDutyCycle(0)
    M4A.ChangeDutyCycle(0)
    M4B.ChangeDutyCycle(0)

def TournerGauche() :
    M2A.ChangeDutyCycle(40)                 #Le moteur à droite "avance"
    M2B.ChangeDutyCycle(0)
    M1A.ChangeDutyCycle(0)                  #Le moteur à gauche "recule"
    M1B.ChangeDutyCycle(40)

def TournerDroite() :
    M1A.ChangeDutyCycle(40)                 #Le moteur à gauche "recule"
    M1B.ChangeDutyCycle(0)
    M2A.ChangeDutyCycle(0)                  #Le moteur à droite "avance"
    M2B.ChangeDutyCycle(40)

#################################################################



#####################        REGLAGES       #####################

camera.framerate = float(24)             #On définit le nombre de fps

Vitesse = 50
avant = 0           #( 0 : arret / 1 : avant / 2 : arrière)

#################################################################



#On démarre affichage en direct
camera.start_preview()

while(True):

    pygame.display.update()

    if filme == True :
        camera.wait_recording()         #On continue de filmer (permet de relever une erreur s'il y a)
                
    for event in pygame.event.get():

        if event.type == KEYDOWN :

            #PHOTOS / VIDEOS :

            if event.key == pygame.K_ESCAPE :
                camera.close()
                pygame.quit()
                sys.exit(0)

            if event.key == pygame.K_RIGHTPAREN :
                camera.capture('Image {}.jpg'.format(time.asctime(time.localtime())))

            if event.key == pygame.K_MINUS :
                if filme == False :
                    camera.start_recording('Video {}.h264'.format(time.asctime(time.localtime())))
                    filme = True
                else :
                    camera.stop_recording()
                    filme = False
            
            if event.key == pygame.K_TAB:
                camera.start_preview()


            #MOTEURS :

            if event.key == K_p :
                if Vitesse <=95 :
                    Vitesse += 5
                    if avant == 1 :             #Si on est en marche avant
                        Avancer(Vitesse)
                    elif avant == 2 :           #Si on est en marche arrière
                        Reculer(Vitesse)

                elif Vitesse < 100 :
                    Vitesse = 100
                    if avant == 1 :
                        Avancer(Vitesse)
                    elif avant == 2 :
                        Reculer(Vitesse)

            if event.key == K_i :
                if Vitesse >= 5 :
                    Vitesse -= 5
                    if avant == 1 :
                        Avancer(Vitesse)
                    elif avant == 2 :
                        Reculer(Vitesse)

                elif Vitesse > 0 :
                    Vitesse = 0
                    if avant == 1 :
                        Avancer(Vitesse)
                    elif avant == 2 :
                        Reculer(Vitesse)

            if event.key == K_o :
                avant = 1
                Avancer(Vitesse)

            if event.key == K_l :
                avant = 2 
                Reculer(Vitesse)

            if event.key == K_LEFT :
                TournerGauche()

            if event.key == K_RIGHT :
                TournerDroite()

            if event.key == K_UP :
                Monter(Vitesse)

            if event.key == K_DOWN :
                Descendre(Vitesse)


            if event.key == K_s :
                avant = 0
                ArretTotal()


        if event.type == KEYUP :

            #MOTEURS :

            
            if event.key == K_o :
                avant = 0
                StopHorizontal()

            if event.key == K_l :
                avant = 0
                StopHorizontal()

            if event.key == K_LEFT :
                avant = 0
                StopHorizontal()

            if event.key == K_RIGHT :
                avant = 0
                StopHorizontal()

            if event.key == K_UP :
                StopVertical()

            if event.key == K_DOWN :
                StopVertical()      

        if event.type == QUIT:
            pygame.display.quit()
            pygame.quit()




