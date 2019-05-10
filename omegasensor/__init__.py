__PACKAGE__ = "omegasensor"
__VERSION__ = "0.1"

from .interface import Smartsensor
try:
    from .bus_i2c import BusI2C, SMARTSENSOR_I2C_ADDR
except Exception as e:
    pass    # platform does not support
from .bus_modbus import BusModbus, SMARTSENSOR_MODBUS_ADDR
from .registers import *
