#!/usr/bin/python

from time import sleep

class Acquario_CommandPlate():

    # definizioni variabili
    _BUZZER_PIN  = 12       # buzzer pin (0 for unused)
    _BUZZER_TYPE = 'ACTIVE' # buzzer type: active (A or ACTIVE) or passive (P or PASSIVE)

    _BTN_PIN_1   = 5  # pin for bit 0 0 0 X
    _BTN_PIN_2   = 6  # pin for bit 0 0 X 0
    _BTN_PIN_4   = 13 # pin for bit 0 X 0 0
    _BTN_PIN_8   = 19 # pin for bit X 0 0 0
    _BTN_BUTTON  = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    _use = {
        'bit_1' : False,
        'bit_2' : False,
        'bit_4' : False,
        'bit_8' : False,
        'buzzer': False
        }

    def __init__(self,
                 pins_btn=[_BTN_PIN_1, _BTN_PIN_2, _BTN_PIN_4, _BTN_PIN_8],
                 buzzer_pin=_BUZZER_PIN, buzzer_type=_BUZZER_TYPE,
                 GPIO=None
                 ):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)

        for f in range(0,15):
            self._BTN_BUTTON[f] = ''

        self._BTN_PIN_1   = pins_btn[0]
        self._BTN_PIN_2   = pins_btn[1]
        self._BTN_PIN_4   = pins_btn[2]
        self._BTN_PIN_8   = pins_btn[3]
        self._BUZZER_PIN  = buzzer_pin
        self._BUZZER_TYPE = buzzer_type.upper()

        if self._BTN_PIN_1 > 0:
            self._use['bit_1'] = True
            self.GPIO.setup(self._BTN_PIN_1, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
            
        if self._BTN_PIN_2 > 0:
            self._use['bit_2'] = True
            self.GPIO.setup(self._BTN_PIN_2, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
            
        if self._BTN_PIN_4 > 0:
            self._use['bit_4'] = True
            self.GPIO.setup(self._BTN_PIN_4, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
            
        if self._BTN_PIN_8 > 0:
            self._use['bit_8'] = True
            self.GPIO.setup(self._BTN_PIN_8, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
            
        if self._BUZZER_PIN > 0:
            self._use['buzzer'] = True
            self.GPIO.setup(self._BUZZER_PIN, self.GPIO.OUT)

        if self._BUZZER_TYPE == 'ACTIVE' or self._BUZZER_TYPE == 'A':
            self._BUZZER_TYPE == 'ACTIVE'
        elif self._BUZZER_TYPE == 'PASSIVE' or self._BUZZER_TYPE == 'P':
            self._BUZZER_TYPE == 'PASSIVE'
        else:
            # force buzzer type active
            self._BUZZER_TYPE == 'ACTIVE'

    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000) # divide microseconds by 1 million for seconds
        sleep(seconds)

    def buzzer(self, second=0.1, freq=0):
        # check if buzzer not used
        if self._use['buzzer'] == False:
            return None

        if self._BUZZER_TYPE == 'ACTIVE':
            self.GPIO.output(self._BUZZER_PIN, self.GPIO.LOW) # start sound
            sleep(second if second > 0 else 0.1)
            self.GPIO.output(self._BUZZER_PIN, self.GPIO.HIGH) # end sound
        else:
            # code for passive buzzer must be create
            pass

    def getButton(self):
        btnTmp = 0
        if self._use['bit_1'] and self.GPIO.input(self._BTN_PIN_1) == False:
            btnTmp += 1
        if self._use['bit_2'] and self.GPIO.input(self._BTN_PIN_2) == False:
            btnTmp += 2
        if self._use['bit_4'] and self.GPIO.input(self._BTN_PIN_4) == False:
            btnTmp += 4
        if self._use['bit_8'] and self.GPIO.input(self._BTN_PIN_8) == False:
            btnTmp += 8

        if btnTmp > 0:
            return self._BTN_BUTTON[btnTmp] if self._BTN_BUTTON[btnTmp] != '' else 'button' + str(btnTmp)
        else:
            return 'none'

    def setButton(self, num, label):
        if 1 <= int(num) <= 15 and str(label) != '':
            self._BTN_BUTTON[int(num)] = str(label)
            return True
        return False



    

if __name__ == '__main__':

    cfgCmdPlate = {
        'buzzer_pin' : 12,
        'buzzer_type': 'ACTIVE',
        'pin_1'      : 5,
        'pin_2'      : 6,
        'pin_4'      : 13,
        'pin_8'      : 19
        }

    objCmdPlate = Acquario_CommandPlate([cfgCmdPlate['pin_1'], cfgCmdPlate['pin_2'], cfgCmdPlate['pin_4'], cfgCmdPlate['pin_8']],
                                        cfgCmdPlate['buzzer_pin'], cfgCmdPlate['buzzer_type'])

    print('Test buzzer')
    objCmdPlate.buzzer(0.1)

    print('Test pulsanti')

    if not objCmdPlate.setButton(1, 'left'):
        print('Errore assegnazione label pulsante 1')
    if not objCmdPlate.setButton(2, 'right'):
        print('Errore assegnazione label pulsante 2')
    if not objCmdPlate.setButton(3, 'up'):
        print('Errore assegnazione label pulsante 3')
    if not objCmdPlate.setButton(4, 'down'):
        print('Errore assegnazione label pulsante 4')
    if not objCmdPlate.setButton(5, 'select'):
        print('Errore assegnazione label pulsante 5')

    while True:
        btn = objCmdPlate.getButton()
        if btn != 'none':
            print(btn)
    
