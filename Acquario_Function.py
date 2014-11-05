#!/usr/bin/python

import time

class Acquario_Function():

    def attesa(self, secondi=0.1):
        time.sleep(secondi)

    def getClockDate(self, formato='%d-%m-%Y'):
         return time.strftime(formato, time.localtime())

    def getClockHour(self, formato='%H:%M'):
         return time.strftime(formato, time.localtime())

    def getDegree(self, valore=0, formato='{0:0.1f}'):
        return formato.format(valore)

class Acquario_Chrono():
    # variabili per cronometro
    _chrono_start = 0
    _chrono_now   = 0
    _chrono_stop  = 0
    _chrono_diff  = 0

    def __init__(self):
        self.reset()

    def reset(self):
        self._chrono_start = 0
        self._chrono_now   = 0
        self._chrono_stop  = 0
        self._chrono_diff  = 0

    def start(self):
        self._chrono_start = time.time()
        self._chrono_now   = 0
        self._chrono_stop  = 0
        self._chrono_diff  = 0

    def stop(self):
        self._chrono_stop = time.time()

    def elapsed(self):
        # se non avviato, lo forza
        if self._chrono_start == 0:
            self.start()
        
        self._chrono_now = time.time() - self._chrono_start
        return self._chrono_now
