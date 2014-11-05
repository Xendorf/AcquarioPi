#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

from Acquario_Config import Acquario_Config
from Acquario_LCD import Acquario_LCD
from Acquario_ThermSensor import *
from Acquario_CommandPlate import Acquario_CommandPlate
from Acquario_Function import Acquario_Function, Acquario_Chrono

objCfg = Acquario_Config()
fn = Acquario_Function()

if not objCfg.ConfigReady():
    print('Verificare la configurazione !!!')
    quit()

if not objCfg.get('system', 'lcd'):
    print('Configurazione Display LCD mancante !!!')
    quit()

if not objCfg.get('system', 'therm'):
    print('Configurazione Sensore di temperatura mancante !!!')
    quit()

if not objCfg.get('system', 'bargraph'):
    print('Configurazione Barra led mancante !!!')
    quit()

if not objCfg.get('system', 'button'):
    print('Configurazione Pulsantiera mancante !!!')
    quit()

cfgLCD = objCfg.get('lcd')
cfgTherm = objCfg.get('therm')
cfgCmdPlate = objCfg.get('btnplate')

objLCD = Acquario_LCD(cfgLCD['pin_rs'], cfgLCD['pin_e'], cfgLCD['pins_db'], cfgLCD['pin_backlight'])

objLCD.begin(cfgLCD['display_cols'], cfgLCD['display_rows'])
objLCD.clear()
objLCD.message('{0}\n{1}'.format(str(cfgLCD['greetings_r1']), str(cfgLCD['greetings_r2'])))

# predisposizione caratteri speciali
objLCD.create_char(1, objLCD.LCD_CHARMAKE['ok'])
objLCD.create_char(2, objLCD.LCD_CHARMAKE['ko'])
objLCD.create_char(3, objLCD.LCD_CHARMAKE['heart'])
objLCD.create_char(4, objLCD.LCD_CHARMAKE['arrow_left'])
objLCD.create_char(5, objLCD.LCD_CHARMAKE['arrow_right'])
objLCD.create_char(6, objLCD.LCD_CHARMAKE['arrow_up'])
objLCD.create_char(7, objLCD.LCD_CHARMAKE['arrow_down'])

lcd_char_ok = '\x01'
lcd_char_ko = '\x02'
lcd_char_heart = '\x03'
lcd_char_left = '\x04'
lcd_char_right = '\x05'
lcd_char_up = '\x06'
lcd_char_down = '\x07'

lcd_char_degree = objLCD.special_char('grade')

fn.attesa()

#    ----------------
t = 'Sensore Temp.  {0}'
objLCD.message(t.format('-'), 1, 2)
fn.attesa()

objTherm = Acquario_ThermSensor()

if not cfgTherm:
    cfgTherm = {
        'type'     : objTherm.get_sensor_value('type'),
        'id'       : objTherm.get_sensor_value('id'),
        'type_name': objTherm.get_sensor_value('type_name'),
        'scan'     : 5
        }
elif not cfgTherm['type']:
    cfgTherm['type'] = objTherm.get_sensor_value('type')
elif not cfgTherm['id']:
    cfgTherm['id'] = objTherm.get_sensor_value('id')
elif not cfgTherm['type_name']:
    cfgTherm['type_name'] = objTherm.get_sensor_value('type_name')

objLCD.message(t.format(lcd_char_ok), 1, 2)
fn.attesa()

t = 'Pulsantiera    {0}'
objLCD.message(t.format('-'), 1, 2)
fn.attesa()

objCmdPlate = Acquario_CommandPlate([cfgCmdPlate['pin_1'], cfgCmdPlate['pin_2'], cfgCmdPlate['pin_4'], cfgCmdPlate['pin_8']], cfgCmdPlate['buzzer_pin'], cfgCmdPlate['buzzer_type'])

objCmdPlate.buzzer(0.1)

objLCD.message(t.format(lcd_char_ok), 1, 2)
fn.attesa()

t = 'Sensore Ph     {0}'
objLCD.message(t.format('-'), 1, 2)
fn.attesa()
objLCD.message(t.format(lcd_char_ko), 1, 2)
fn.attesa()

t = 'Barra Led      {0}'
objLCD.message(t.format('-'), 1, 2)
fn.attesa()
objLCD.message(t.format(lcd_char_ko), 1, 2)
fn.attesa()

# un po' di effetti non guastano mai
for row in range(1,3):
    for col in range(1,17):
        objLCD.message('*', col, row)
        fn.attesa(0.01)
for row in range(1,3):
    for col in range(1,17):
        objLCD.message(' ', col, row)
        fn.attesa(0.01)

try:

    # inizializza ed avvia i cronometri
    chronoTherm = Acquario_Chrono()
    chronoTherm.start()

    # inizializza il dizionario per i valori ottenuti dalle scansioni
    arrSensori = {
        'gradi_attuali'   : 0,
        'gradi_precedenti': 0,
        }
    
    
    while True:
        strOra = fn.getClockHour('%H:%M')
        #objLCD.message(fn.getClockDate('%d-%m'), 1, 1)
        objLCD.message(strOra, 17 - len(strOra), 1)

        if chronoTherm.elapsed() >= cfgTherm['scan']:
            objLCD.message(lcd_char_heart, 1,1)
            # storicizza il precedente rilevamento ed ottiene quello nuovo
            arrSensori['gradi_precedenti'] = arrSensori['gradi_attuali']
            arrSensori['gradi_attuali'] = objTherm.get_temperature(objTherm.DEGREES_C)

            # imposta la stringa di visualizzazione su LCD
            strTemperatura = fn.getDegree(arrSensori['gradi_attuali']) + lcd_char_degree + 'C'

            # se la temperatura precedente Ã¨ stata valorizzata verifica se
            # la temperatura Ã¨ stabile, diminuita o cresciuta aggiungendo
            # anche i caratteri alla stringa di visualizzazione su LCD
            if arrSensori['gradi_precedenti'] > 0:
                if arrSensori['gradi_precedenti'] < arrSensori['gradi_attuali']:
                    strTemperatura += lcd_char_up
                elif arrSensori['gradi_precedenti'] > arrSensori['gradi_attuali']:
                    strTemperatura += lcd_char_down
                else:
                    strTemperatura += ' '
            
            objLCD.message(strTemperatura, 1, 2)
            # resetta il cronometro per la scansione della temperatura
            chronoTherm.reset()
            objLCD.message(' ', 1,1)
        
        

except KeyboardInterrupt:
    quit()


