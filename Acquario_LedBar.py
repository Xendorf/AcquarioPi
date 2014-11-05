#!/usr/bin/python

from time import sleep

class Acquario_LedBar():

    # impostazioni iniziali dei led
    _led = range(0,25)

    SPENTO = 0
    VERDE = 1
    ROSSO = 2
    GIALLO = 3


    def __init__(self):
        
        from Adafruit_LED_Backpack import BicolorBargraph24

        #prima barra
        self._led[0]  = VERDE
        self._led[1]  = VERDE
        self._led[2]  = VERDE
        self._led[3]  = VERDE
        self._led[4]  = GIALLO
        self._led[5]  = GIALLO
        self._led[6]  = GIALLO
        self._led[7]  = GIALLO
        self._led[8]  = ROSSO
        self._led[9]  = ROSSO
        self._led[10] = ROSSO
        self._led[11] = ROSSO
        # seconda barra
        self._led[12] = VERDE
        self._led[13] = VERDE
        self._led[14] = VERDE
        self._led[15] = VERDE
        self._led[16] = GIALLO
        self._led[17] = GIALLO
        self._led[18] = GIALLO
        self._led[19] = GIALLO
        self._led[20] = ROSSO
        self._led[21] = ROSSO
        self._led[22] = ROSSO
        self._led[23] = ROSSO

        self._BarGraph = BicolorBargraph24.BicolorBargraph24()
        self._BarGraph.begin()

    def setLuminosita(self, brightness=0):

        if 0 <= brightness <= 15:
            self._BarGraph.set_brightness(brightness)


if __name__ == '__main__':

