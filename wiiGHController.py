########################################################
## Python module to read a Wii Guitar Hero Controller ##
##                                                    ##
## By Tim Dobbert                                     ##
## analog.sketchbook.101@gmail.com                    ##
##                                                    ##
## Adapted from library for standard Wii Nunchuck     ##
## by Jason - @Boeeerb                                ##
##  jase@boeeerb.co.uk                                ##
########################################################

## Revision history from original standard nunchuck library
## v0.1 03/05/14 - Initital release
## v0.2 21/06/14 - Retrieve one byte at a time [Simon Walters - @cymplecy]
## v0.3 22/06/14 - Minor Refactoring [Jack Wearden - @JackWeirdy]
## v0.32 25/6/14 - XOR each data byte with 0x17 and then add 0x17 to produce corrent values - Simon Walters @cymplecy
## v0.4 26/6/14 - Change method of XOR and add delay parameter - Simon Walters @cymplecy
## v0.41 30/3/15 - Adding support for RPI_REVISION 3 - John Lumley @Jelby-John

from smbus import SMBus
import RPi.GPIO as rpi
import time as time

bus = 0

class GuitarHeroController:

  def __init__(self,delay = 0.05):
    self.buttonUp = False
    self.buttonDown = False
    self.buttonOrange = False
    self.buttonBlue = False
    self.buttonYellow = False
    self.buttonRed = False
    self.buttonGreen = False
    self.buttonPlus = False
    self.buttonMinus = False
    self.whammyBar = None
    
    self.delay = delay
    if rpi.RPI_REVISION == 1:
      self.i2c_bus = 0
    elif rpi.RPI_REVISION == 2:
      self.i2c_bus = 1
    elif rpi.RPI_REVISION == 3:
      self.i2c_bus = 1
    else:
      print("Unable to determine Raspberry Pi revision.")
      exit
    self.bus = SMBus(self.i2c_bus)
    self.bus.write_byte_data(0x52,0x40,0x55)
    time.sleep(0.015)
    self.bus.write_byte_data(0x52,0x40,0x00)
    time.sleep(0.015)
  
  def restart(self):
    self.bus = SMBus(self.i2c_bus)
    self.bus.write_byte_data(0x52,0x40,0x55)
    time.sleep(0.015)
    self.bus.write_byte_data(0x52,0x40,0x00)
    time.sleep(0.015)
            
  def read(self):
      self.bus.write_byte(0x52,0x00)
      time.sleep(self.delay)
      temp = [(0x17 + (0x17 ^ self.bus.read_byte(0x52))) for i in range(6)]
      return temp

  def raw(self):
    data = self.read()
    return data

  # Guitar Hero Mappings
  def button_up(self):
    data = self.read()
    bu = (data[5] & 0x01)
    return bu == 0

  def button_down(self):
    data = self.read()
    bd = (data[4] >> 6) & 0x01
    return bd == 0

  def button_orange(self):
    data = self.read()
    bo = (data[5] >> 7) & 0x01
    return bo == 0

  def button_blue(self):
    data = self.read()
    bb = (data[5] >> 5) & 0x01
    return bb == 0

  def button_yellow(self):
    data = self.read()
    by = (data[5] >> 3) & 0x01
    return by == 0

  def button_red(self):
    data = self.read()
    br = (data[5] >> 6) & 0x01
    return br == 0

  def button_green(self):
    data = self.read()
    bo = (data[5] >> 4) & 0x01
    return bo == 0

  def button_plus(self):
    data = self.read()
    bp = (data[4] >> 2) & 0x01
    return bp == 0

  def button_minus(self):
    data = self.read()
    bm = (data[4] >> 4) & 0x01
    return bm == 0
  
  def whammy_bar(self):
      data = self.read()
      fullbyte = bin(data[3])
      nibble = fullbyte[6:]
      return int(nibble,2) # returns val between 1 and 15

  def joystick_x(self):
    data = self.read()
    fullbyte = bin(data[0])
    lastSix = fullbyte[4:]
    return int(lastSix, 2) # returns val 0-64 or so

  def joystick_y(self):
    data = self.read()
    fullbyte = bin(data[1])
    lastSix = fullbyte[4:]
    return int(lastSix, 2) # returns val 0-64 or so
    
  def setdelay(self,delay):
    self.delay = delay

  def scale(self,value,_min,_max,_omin,_omax):
    return (value - _min) * (_omax - _omin) // (_max - _min) + _omin

  def readAll(self):
      self.buttonUp = self.button_up()
      self.buttonDown = self.button_down()
      self.buttonOrange = self.button_orange()
      self.buttonBlue = self.button_blue()
      self.buttonYellow = self.button_yellow()
      self.buttonRed = self.button_red()
      self.buttonGreen = self.button_green()
      self.buttonPlus = self.button_plus()
      self.buttonMinus = self.button_minus()
      self.whammyBar = self.whammy_bar()
      self.joystickX = self.joystick_x()
      self.joystickY = self.joystick_y()