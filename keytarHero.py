########################################################
#                   Keytar Hero                        #
#              Created by Tim Dobbert                  #
#           analog.sketchbook.101@gmail.com            #
########################################################

# Synthesizer that uses a Wii Guitar Hero Controller and a Raspberry Pi 
# (I'm using 3 B+) to control a software synthesizer built in Pure Data (Pd).
# The main purpose of the code below is to launch the Pure Data patch
# and then feed the controller's signal on to the patch in realtime

import wiiGHController
import time, os, subprocess

DONE = False
PD_PATCH_PATH = "/home/pi/keytarHero/keytarHero.pd"   # path to your Pd patch

def send2Pd(message):
    '''Sends messages to the Pure Data patch via udp'''
    os.system("echo '" + message + "' | pdsend 5400 localhost udp")
    
def main(): # main loop function
   DONE = False
   guitar = wiiGHController.GuitarHeroController(delay=.01)
   subprocess.call("pd %s &" % PD_PATCH_PATH, shell=True)
   
   while 1:
      while not(DONE):
         try:
             guitar.readAll()
             # A bit of funky type casting here but Pd doesn't understand bools
             # so we cast the bool as an int, then cast the int to a string that
             # can be concatenated so we can pass the data all at once via udp.
             # The Pd patch can then unpack that string into numbers again.
             # This will allow the patch to work with all of the various signals
             # coming from the guitar simultaneously.
             message = str(int(guitar.buttonOrange))+' '+\
                       str(int(guitar.buttonBlue))+' ' +\
                       str(int(guitar.buttonYellow))+' ' +\
                       str(int(guitar.buttonRed))+' ' +\
                       str(int(guitar.buttonGreen))+' ' +\
                       str(int(guitar.buttonUp))+' ' +\
                       str(int(guitar.buttonDown))+' ' +\
                       str(int(guitar.buttonPlus))+' ' +\
                       str(int(guitar.buttonMinus))+' ' +\
                       str(guitar.whammyBar)+' ' +\
                       str(guitar.joystick_x())+' ' +\
                       str(guitar.joystick_y())+' '
             print(message) # uncomment for debugging
             send2Pd(message)
         except:
             pass
         
      DONE = False

# Main program logic:
if __name__ == '__main__':
    main()
