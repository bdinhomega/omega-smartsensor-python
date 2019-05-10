import smbus
import struct
from .bus import Bus, bus_logger

SMARTSENSOR_I2C_ADDR = 0x68


class BusI2C(Bus):

    def __init__(self, bus_id, dev_addr):
        """
            Initialize Bus I2C with bus id for device address on the bus
        :param bus_id: bus id (eg:1, 2, ...)
        :param dev_addr: device address
        """
        super().__init__(Bus.Type.I2C, dev_addr)
        self.bus = smbus.SMBus(bus_id)

    def read_register(self, reg_addr, bytes_cnt):
        """
            Read from i2c register address with bytes count
        :param reg_addr: i2c register address
        :param bytes_cnt: bytes count
        :return: bytes
        """
        data = self.read_bytes(reg_addr, bytes_cnt)
        bus_logger.debug("Read 0x%04x <= %s" % (reg_addr, data))
        return data

    def write_register(self, reg_addr, data):
        """
            Write to i2c register address with provided data
        :param reg_addr: i2c register address
        :param data: data bytes in list
        """
        assert(type(data) is list)
        bus_logger.debug("Write 0x%04x => %s" % (reg_addr, data))
        self.write_bytes(reg_addr, data)

    def read_byte(self, reg_addr):
        """
            Read a byte from i2c register address
        :param reg_addr: i2c register address
        :return: byte data
        """
        data = self.bus.read_byte(reg_addr)
        return data

    def read_float(self, reg_addr):
        """
            Read a float from i2c register address
        :param reg_addr: i2c register address
        :return: float data
        """
        data = self.bus.read_i2c_block_data(self.dev_addr, reg_addr, 4)
        value, = struct.unpack('>f', bytearray(data))
        return value

    def read_uint32(self, reg_addr):
        """
            Read uint32 from i2c register address
        :param reg_addr: i2c register address
        :return: int data
        """
        data = self.bus.read_i2c_block_data(self.dev_addr, reg_addr, 4)
        value, = struct.unpack('>I', bytearray(data))
        return value

    def read_uint16(self, reg_addr):
        """
            Read uint16 from i2c register address
        :param reg_addr: i2c register address
        :return: int data
        """
        data = self.bus.read_i2c_block_data(self.dev_addr, reg_addr, 2)
        value, = struct.unpack('>H', bytearray(data))
        return value

    def read_bytes(self, reg_addr, cnt):
        """
            Read bytes with count from i2c register address
        :param reg_addr: i2c register address
        :param cnt: bytes count
        :return: bytes
        """
        data = self.bus.read_i2c_block_data(self.dev_addr, reg_addr, cnt)
        return data

    def write_byte(self, reg_addr, data):
        """
            Write bytes to i2c register address
        :param reg_addr: i2c register address
        :param data: bytes
        """
        self.bus.write_byte(reg_addr, data)

    def write_float(self, reg_addr, value: float):
        """
            Write float value to i2c register address
        :param reg_addr: i2c register address
        :param value: float value
        """
        data = struct.pack('>f', value)
        self.bus.write_block_data(self.dev_addr, reg_addr, data)

    def write_uint32(self, reg_addr, value: int):
        """
            Write uint32 value to i2c register address
        :param reg_addr: i2c register address
        :param value: int value
        """
        data = struct.pack(">I", value)
        self.bus.write_block_data(self.dev_addr, reg_addr, data)

    def write_uint16(self, reg_addr, value: int):
        """
            Write uint16 value to i2c register address
        :param reg_addr: i2c register address
        :param value: int value
        """
        data = struct.pack(">H", value)
        self.bus.write_block_data(self.dev_addr, reg_addr, data)

    def write_bytes(self, reg_addr, data: bytearray):
        """
            Write bytes to i2c register address
        :param reg_addr: i2c register address
        :param data: bytes
        """
        self.bus.write_i2c_block_data(self.dev_addr, reg_addr, data)
