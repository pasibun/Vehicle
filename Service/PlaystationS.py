import pygame
import sys
import time
from pygame import QUIT, JOYAXISMOTION, KEYDOWN, K_UP, K_DOWN, K_RETURN, JOYBUTTONDOWN, K_ESCAPE
from pygame import joystick


class PlaystationService:
    # Initialise the pygame library
    pygame.init()
    pygame.joystick.init()

    assen = None
    knoppen = None
    asrichting = 0
    ps3Connected = False

    def __init__(self):
        print("")
        print("Joystick initializing...")
        if pygame.joystick.get_count() == 0:
            print("ERROR! Did not found a joystick!")
            time.sleep(2)
            print("")
            print("Keyboard initializing...")
            self.keyboardcontrole()
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            print("Joysticks gevonden:", pygame.joystick.get_count(), "(", joystick.get_name(), ")")
            print("Specs: assen:", joystick.get_numaxes(), ", knoppen:", joystick.get_numbuttons())
            self.knoppen = joystick.get_numbuttons()
            self.assen = joystick.get_numaxes()
            self.ps3Connected = True

    def joystickcontrole(self):
        try:
            while self.ps3Connected:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.quit_game()
                    if event.type == JOYBUTTONDOWN:
                        for i in range(self.knoppen):
                            # Haal de waarde van de knop op.
                            knop = joystick.get_button(i)
                            if knop == 1:
                                print("Knop:", i, "ingedrukt!")
                    if event.type == JOYAXISMOTION:
                        if event.dict['axis'] == 1:
                            for i in range(self.assen):
                                # Haal de waarde van de as op.
                                eenas = joystick.get_axis(i)
                                if eenas != 0:
                                    if i == 0: self.asrichting = 'X'
                                    if i == 1: self.asrichting = 'Y'
                                    if i == 2: self.asrichting = 'X'
                                    if i == 3: self.asrichting = 'Y'
                                print("AS", i, "waarde:", self.asrichting, eenas)
        except KeyboardInterrupt:
            pygame.quit()

    def keyboardcontrole(self):
        try:
            time.sleep(2)
            print("Making keyboard ready for controlling..")
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    print(event.type)
                    if event.key == K_ESCAPE:
                        self.quit_game()
                    if event.key == K_DOWN:
                        print('down')
                    if event.key == K_UP:
                        print('up')
                    if event.key == K_RETURN:
                        print('enter')

        except:
            print("ERROR! Keyboard control is broke.", pygame, pygame.event)
            pygame.quit()

    def quit_game(self):
        print("Exiting program.")
        pygame.quit()
        sys.exit()
