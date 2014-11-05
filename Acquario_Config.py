#!/usr/bin/python

class Acquario_Config():

    # variabili generiche
    CFG_PRINT = True # utilizza il comando print per stampare a video

    """
    in questa prima release i valori di configurazione sono inseriti direttamente nel
    codice con la prospettiva futura di inserire un sistema vero e proprio di gestione
    della configurazione
    """
    def __init__(self, GPIO=None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self._config = {}

        # impostazioni di sistema generali
        self._config['system'] = {
            'pi_revision': 3,
            'scan'       : 5,
            'ready'      : False,
            'lcd'        : True,
            'therm'      : True,
            'bargraph'   : True,
            'button'     : True,
            }

        if self._valid_pi_revision() == True:
            self._config['system']['ready'] = True
            # continue loading other settings

            self._config['lcd'] = {
                'display_rows' : 2,
                'display_cols' : 16,
                'pin_rs'       : 14,
                'pin_e'        : 15,
                'pins_db'      : [17, 18, 27, 22],
                'pin_backlight': None,
                # testo iniziale  ----------------
                'greetings_r1' : '  Acquario RPi  ',
                'greetings_r2' : 'attendere  prego'
                }

            self._config['therm'] = {
                'id'           : '000005aba251',
                'type'         : 40,
                'type_name'    : 'DS18B20',
                'min'          : 25,
                'max'          : 27,
                'scan'         : 5 # tempo in secondi tra un rilevamento e l'altro
                }
            
            self._config['btnplate'] = {
                'buzzer_pin': 12,
                'buzzer_type': 'ACTIVE',
                'pin_1' : 5,
                'pin_2' : 6,
                'pin_4' : 13,
                'pin_8' : 0,
                'left'  : 1,
                'right' : 2,
                'up'    : 3,
                'down'  : 4,
                'select': 5
                }
        else:
            print('Revisione Pi attuale ({0}) non adatta: necessaria revisione {1}'.format(str(self.GPIO.RPI_REVISION), self._config['system']['pi_revision']))


    def _valid_pi_revision(self):
        if self.GPIO.RPI_REVISION == self._config['system']['pi_revision']:
            return True
        return False

    def ConfigReady(self):
        return self._config['system']['ready']

    def get(self, what_device, what_value=''):
        if what_device in self._config:
            if what_value != '':
                if what_value in self._config[what_device]:
                    return self._config[what_device][what_value]
            else:
                return self._config[what_device]
        return None

if __name__ == '__main__':

    objCfg = Acquario_config()


