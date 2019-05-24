import pygame
from pygame import display, joystick, event
from pygame import QUIT, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN

class PlaystationControl:
    # Initialise the pygame library
    pygame.init()
    pygame.joystick.init()

    assen = None
    knoppen = None
    asrichting = 0
    ps3Connected = False

    def __init__(self):
        print("Playstation controller initialize...")
        if(pygame.joystick.get_count() == 0):
            print("Er is geen joystick gevonden!")
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            
            print("Joysticks gevonden:", pygame.joystick.get_count(), "(", joystick.get_name(), ")")
            print("Specs: assen:", joystick.get_numaxes(), ", knoppen:", joystick.get_numbuttons())
            self.knoppen = joystick.get_numbuttons()
            self.assen = joystick.get_numaxes()
            self.ps3Connected = True
            
    def controlingJoystick():
        try:
            while ps3Connected:
                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        print("doe iets met quit")
                    if(event.type == pygame.JOYBUTTONDOWN):
                        for i in range(knoppen):
                            # Haal de waarde van de knop op.
                            knop = joystick.get_button(i)
                            if (knop == 1):
                                print("Knop:", i, "ingedrukt!")
                    if (event.type == pygame.JOYAXISMOTION):
                        if (event.dict['axis'] == 1):
                            for i in range(assen):
                                # Haal de waarde van de as op.
                                eenas = joystick.get_axis(i)
                                if(eenas != 0):
                                    if (i == 0): asrichting = 'X'
                                    if (i == 1): asrichting = 'Y'
                                    if (i == 2): asrichting = 'X'
                                    if (i == 3): asrichting = 'Y'
                                print("AS", i, "waarde:", asrichting, eenas)
        except KeyboardInterrupt:
            pygame.quit()