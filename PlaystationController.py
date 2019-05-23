import pygame as pg, driving

# Initialise the pygame library
pg.init()
pg.joystick.init()

assen = None
knoppen = None
asrichting = 0
ps3Connected = False

class PlaystationControl:
    def initializeControler():
        print("Playstation controller initialize..."
        if pygame.joystick.get_count() == 0:
            print "Er is geen joystick gevonden!"
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            
            print "Joysticks gevonden:", pg.joystick.get_count(), "(", joystick.get_name(), ")"
            print "Specs: assen:", joystick.get_numaxes(), ", knoppen:", joystick.get_numbuttons()
            knoppen = joystick.get_numbuttons()
            assen = joystick.get_numaxes()
            ps3Connected = True
        return ps3Connected

            
    def controlingJoystick():
        try:
            while ps3Connected:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        #doe iets met quit
                    if event.type == pg.JOYBUTTONDOWN:
                        for i in range(knoppen):
                            # Haal de waarde van de knop op.
                            knop = joystick.get_button(i)
                            if knop == 1:
                                print("Knop:", i, "ingedrukt!")
                    if event.type == pg.JOYAXISMOTION:
                        if event.dict['axis'] == 1:
                            for i in range(assen):
                                # Haal de waarde van de as op.
                                eenas = joystick.get_axis(i)
                                # Als een as
                                if eenas <> 0:
                                    if i == 0: asrichting = 'X'
                                    if i == 1: asrichting = 'Y'
                                    if i == 2: asrichting = 'X'
                                    if i == 3: asrichting = 'Y'
                                print "AS", i, "waarde:", asrichting, eenas
        except KeyboardInterrupt:
            pg.quit()