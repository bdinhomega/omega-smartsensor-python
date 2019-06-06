from omegasensor.bus_modbus import BusModbus
from omegasensor.registers import *
from omegasensor.interface import Smartsensor
from omegasensor.smartsensor import _def, _PR


def test_io_read():
    bus = BusModbus('/dev/ttyUSB1', 1)
    bus.debug = 0
    ss = Smartsensor(bus)

    for reg in R:
        if _def[reg]["Access"] == _PR:
            continue
        if reg in [R.EXTRACT_END_TIME, R.NUMBER_OF_RECORDS]:
            continue
        try:
            data = ss.read(reg)
        except:
            print("Has problem: ", reg)


test_io_read()