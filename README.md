# Keytar Hero
Library for Wii Guitar Hero + Raspberry Pi + Pure Data

The code in this repository allows you to connect a Guitar Hero Wii Controller to a Raspberry Pi and use it to control a Pure Data patch. It includes:
  --wiiGHController.py: Python library for i2c communication to the controller
  --keytarHero.py: Python script that launches Pure Data and establishes a connection between the guitar controller and the keytarHero.pd Pure Data patch.
  --keytarHero.pd: A Pure Data patch that reads the guitar controller signal and generates sequenced sounds.
  --setupInstructions.txt: Complete instructions on setting up the Raspberry Pi, Pure Data, and the hardware connection between the Raspberry Pi and the Wii GuitarHero Controller
  
  Note: This has only been tested on the Raspberry Pi 3 B+ but should theoretically work on the 4 as well. The controller library doesn't work for the Touchbar version of the Guitar, but could be modified to do so.
