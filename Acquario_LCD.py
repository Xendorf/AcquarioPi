#!/usr/bin/python

from time import sleep, strftime, localtime

class Acquario_LCD:

    # backlight
    LCD_INVERTPOLARITY      = True
    LCD_INITIALBACKLIGHT    = 1.0

    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00

    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00

    # dictionary for special char
    LCD_SPECIALCHAR_UNKNOW  = 0xFF
    LCD_SPECIALCHAR         = {
        'grade'   : 0xDF,
        'ohm'     : 0xF4,
        'micro'   : 0xE4,
        'sum'     : 0xF6,
        'pi'      : 0xF7,
        'divide'  : 0xFD,
        'square'  : 0xDB,
        'infinite': 0xF3
        }
    # dictionary for char maker
    LCD_CHARMAKE            = {
        'heart'      : [0,0,10,31,31,14,4,0],
        'arrow_left' : [0,2,6,14,6,2,0,0],
        'arrow_right': [0,8,12,14,12,8,0,0],
        'arrow_up'   : [0,0,4,14,31,0,0,0],
        'arrow_down' : [0,0,31,14,4,0,0,0],
        'clock'      : [0,14,21,23,17,14,0,0],
        'clock_t1'   : [0,4,4,4,4,4,0,0],
        'clock_t2'   : [0,1,2,4,8,16,0,0],
        'clock_t3'   : [0,0,0,31,0,0,0,0],
        'clock_t4'   : [0,16,8,4,2,1,0,0],
        'ok'         : [0,1,3,22,28,8,0,0],
        'ko'         : [0,27,14,4,14,27,0,0]
        }


    def __init__(self, pin_rs=14, pin_e=15, pins_db=[17, 18, 27, 22], pin_backlight=None, GPIO = None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
        self.pin_backlight = pin_backlight
        self._blpol = not self.LCD_INVERTPOLARITY

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_e, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)

        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)

        if pin_backlight is not None:
            self.GPIO.setup(self.pin_backlight, GPIO.OUT)
            self.GPIO.output(self.pin_backlight, self._blpol if self.LCD_INITIALBACKLIGHT else not self._blpol)

        self.write4bits(0x33) # initialization
        self.write4bits(0x32) # initialization
        self.write4bits(0x28) # 2 line 5x7 matrix
        self.write4bits(0x0C) # turn cursor off 0x0E to enable cursor
        self.write4bits(0x06) # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        """ Initialize to default text direction (for romance languages) """
        self.displaymode =  self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode) #  set the entry mode

        self.clear()


    def begin(self, cols, lines):
        if (lines > 1):
            self.numlines = lines
            self.displayfunction |= self.LCD_2LINE
            self.currline = 0
        self._cols = cols
        self._lines = lines

    def home(self):
        self.write4bits(self.LCD_RETURNHOME)    # set cursor position to zero
        self.delayMicroseconds(3000)    # this command takes a long time!


    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY)  # command to clear display
        self.delayMicroseconds(3000)    # 3000 microsecond sleep, clearing the display takes a long time

    def set_cursor(self, col, row):
        self.row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]

        if ( row > self.numlines ):
            row = self.numlines - 1 # we count rows starting w/0

        self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    def display(self, status=True):
        """ Turn the display on/off (quickly) """
        if status == True:
            self.displaycontrol |= self.LCD_DISPLAYON
        else:
            self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self, status=True):
        """ Turn the cursor on/off (quickly) """
        if status == True:
            self.displaycontrol |= self.LCD_CURSORON
        else:
            self.displaycontrol &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self, status=True):
        """ Turn on and off the blinking cursor """
        if status == True:
            self.displaycontrol |= self.LCD_BLINKON
        else:
            self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def move_left(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def move_right(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT);

    def set_backlight(self, backlight=True):
        # Enable or disable the backlight
        if self.pin_backlight is not None:
            self.GPIO.output(self.pin_backlight, self._blpol if not backlight else not self._blpol)

    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
        self.delayMicroseconds(1000) # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8)
        self.GPIO.output(self.pin_rs, char_mode)

        #for pin in self.pins_db:
        #    self.GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)
            else:
                self.GPIO.output(self.pins_db[::-1][i], False)

        self.pulseEnable()

        #for pin in self.pins_db:
        #    self.GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)
            else:
                self.GPIO.output(self.pins_db[::-1][i-4], False)

        self.pulseEnable()


    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000) # divide microseconds by 1 million for seconds
        sleep(seconds)


    def pulseEnable(self):
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, True)
        self.delayMicroseconds(1) # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1) # commands need > 37us to settle


    def message(self, text, col=None, row=None):
        """ Send string to LCD. Newline wraps to second line"""

        if col != None and row != None:
            self.set_cursor((col - 1), (row - 1))
        
        for char in text:
            if char == '\n':
                self.write4bits(0xC0) # next line
            else:
                self.write4bits(ord(char),True)

    def special_char(self, sp_char):
        return chr(self.LCD_SPECIALCHAR.get(sp_char, self.LCD_SPECIALCHAR_UNKNOW))

    def create_char(self, location, pattern):
        # solo la posizione da 0 a 7 son consentite
        location &= 0x7
        self.write4bits(self.LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self.write4bits(pattern[i], char_mode=True)

if __name__ == '__main__':

    objLCD = Acquario_LCD(14, 15, [17, 18, 27, 22])
    objLCD.begin(16, 2)
    objLCD.clear()
    objLCD.message('{0}\n{1}'.format('ABCDEFGHIJKLMNOP', '1234567890123456'))

    # predisposizione caratteri speciali
    lcd_char_ok = '\x01'
    objLCD.create_char(1, objLCD.LCD_CHARMAKE['ok'])
    lcd_char_ko = '\x02'
    objLCD.create_char(2, objLCD.LCD_CHARMAKE['ko'])
    lcd_char_heart = '\x03'
    objLCD.create_char(3, objLCD.LCD_CHARMAKE['heart'])
    sleep(3)
    objLCD.message('\x01 \x02 \x03 \x04         \nABCDEFGHIJKLMNOP')

