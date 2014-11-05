#!/usr/bin/python

from time import sleep

class Acquario_LedBar():

    # impostazioni iniziali dei led
    _led = range(0,24)

    SPENTO = 0
    VERDE = 1
    ROSSO = 2
    GIALLO = 3

    def __init__(self):
        
        from Adafruit_LED_Backpack import BicolorBargraph24

        for i in range(0,4):
            #prima barra
            self._led[i] = VERDE
            self._led[i+4] = GIALLO
            self._led[i+8] = ROSSO
            #seconda barra
            self._led[i+12] = VERDE
            self._led[i+16] = GIALLO
            self._led[i+20] = ROSSO
            
        self._BarGraph = BicolorBargraph24.BicolorBargraph24()
        self._BarGraph.begin()

    def setLuminosita(self, brightness=0):

        if 0 <= brightness <= 15:
            self._BarGraph.set_brightness(brightness)


if __name__ == '__main__':

