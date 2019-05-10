from enum import Enum
import logging

logging.basicConfig()
bus_logger = logging.getLogger('[Bus]')
bus_logger.setLevel(logging.INFO)


class Bus:
    class Type(Enum):
        I2C = 0
        Modbus = 1

    def __init__(self, bus_type: Type, dev_addr):
        """
            Base class for supported bus
        :param bus_type: bus type
        :param dev_addr: device address on the bus
        """
        self.bus_type = bus_type
        self.dev_addr = dev_addr
        self._debug = False

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value
        if value:
            bus_logger.setLevel(logging.DEBUG)
        else:
            bus_logger.setLevel(logging.INFO)

    def read_register(self, reg_addr, bytes_cnt):
        """
            Stub function
        :param reg_addr:  register address
        :param bytes_cnt: bytes count
        """
        raise NotImplemented

    def write_register(self, reg_addr, data):
        """
            Stub function
        :param reg_addr: register address
        :param data:  bytes data
        """
        raise NotImplemented
