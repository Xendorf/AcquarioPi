#!/usr/bin/python

import errno
from os import path, listdir, system

class Acquario_ThermSensor(object):

    # sensor directory name start with ...
    THERM_SENSOR_DS18S20 = 0x10 # ... 10-xxxxxxxxxxxx
    THERM_SENSOR_DS1822  = 0x22 # ... 22-xxxxxxxxxxxx
    THERM_SENSOR_DS18B20 = 0x28 # ... 28-xxxxxxxxxxxx

    # public constant
    DEGREES_C            = 0x01 # Celsius
    DEGREES_F            = 0x02 # Fahrenheit
    DEGREES_K            = 0x03 # Kelvin
    UNIT_FACTORS         = {
        DEGREES_C: lambda x: x * 0.001,
        DEGREES_F: lambda x: x * 0.001 * 1.8 + 32.0,
        DEGREES_K: lambda x: x * 0.001 + 273.15
        }
    TYPE_NAMES = {
        THERM_SENSOR_DS18S20: "DS18S20",
        THERM_SENSOR_DS1822: "DS1822",
        THERM_SENSOR_DS18B20: "DS18B20"
        }
    RESOLVE_TYPE_STR = {
        "10": THERM_SENSOR_DS18S20,
        "22": THERM_SENSOR_DS1822,
        "28": THERM_SENSOR_DS18B20
        }

    #private constant
    _BASE_DIRECTORY      = '/sys/bus/w1/devices'
    _SLAVE_FILE          = 'w1_slave'
    _LOAD_KERNEL_MODULES = True

    @classmethod
    def get_available_sensors(cls, types=[THERM_SENSOR_DS18S20, THERM_SENSOR_DS1822, THERM_SENSOR_DS18B20]):
        # Returns all available sensors
        is_sensor = lambda s: any(s.startswith(hex(x)[2:]) for x in types)
        return [cls(cls.RESOLVE_TYPE_STR[s[:2]], s[3:]) for s in listdir(cls._BASE_DIRECTORY) if is_sensor(s)]

    def __init__(self, sensor_type=None, sensor_id=None):
        #If no sensor id is given the first found sensor will be taken
        self._type = sensor_type
        self._id = sensor_id

        if self._LOAD_KERNEL_MODULES:
            self._load_kernel_modules()

        if not sensor_type and not sensor_id:
            s = self.get_available_sensors()
            if not s:
                return None
            self._type, self._id = s[0].type, s[0].id
        elif not sensor_id:
            s = self.get_available_sensors([sensor_type])
            if not s:
                return None
            self._id = s[0].id

        self._sensorpath = self.sensorpath

    @property
    def id(self):
        # Returns the id of the sensor
        return self._id

    @property
    def type(self):
        # Returns the type of this temperature sensor
        return self._type

    @property
    def type_name(self):
        # Returns the type name of this temperature sensor
        return self.TYPE_NAMES.get(self._type, "Sconosciuto")

    @property
    def slave_prefix(self):
        # Returns the slave prefix for this temperature sensor
        return "%s-" % hex(self._type)[2:]

    @property
    def sensorpath(self):
        # Returns the sensors slave path
        sensor_path = path.join(self._BASE_DIRECTORY, self.slave_prefix + self._id, self._SLAVE_FILE)
        if not path.exists(sensor_path):
            return 'NoSensorFound'

        return sensor_path

    @property
    def raw_sensor_value(self):
        # Returns the raw sensor value
        with open(self.sensorpath, "r") as f:
            data = f.readlines()

        if data[0].strip()[-3:] != "YES":
            return 'SensorNotReady'
        return float(data[1].split("=")[1])

    def _get_unit_factor(self, unit):
        # Returns the unit factor depending on the unit constant
        return self.UNIT_FACTORS[unit]

    def get_temperature(self, unit=DEGREES_C):
        # Returns the temperature in the specified unit
        # -original- factor = self._get_unit_factor(unit)
        # -original- return factor(self.raw_sensor_value)
        sensor_value = self.raw_sensor_value
        return self._get_unit_factor(unit)(sensor_value)

    def get_temperatures(self, units):
        # Returns the temperatures in the specified units
        sensor_value = self.raw_sensor_value
        return [self._get_unit_factor(unit)(sensor_value) for unit in units]

    def get_sensor_value(self, what_value):
        if what_value == 'id':
            return self._id
        elif what_value == 'type':
            return self._type
        elif what_value == 'type_name':
            return self.TYPE_NAMES.get(self._type, "Sconosciuto")

    def _load_kernel_modules(self):
        # Load kernel modules needed by the temperature sensor
        try:
            tryDir = listdir(self._BASE_DIRECTORY)
        except OSError as e:
            if e.errno == errno.ENOENT:
                system("modprobe w1-gpio")
                system("modprobe w1-therm")

if __name__ == '__main__':

    from time import sleep
    objSensori = Acquario_ThermSensor()

    while True:
        sleep(0.5)
        tCelsius, tFahrenheit, tKelvin = objSensori.get_temperatures([objSensori.DEGREES_C, objSensori.DEGREES_F, objSensori.DEGREES_K])
        strTherm = '{0:0.2f} C {1:0.2f} F {1:0.2f} K'.format(tCelsius, tFahrenheit, tKelvin)
        print(strTherm)

