import minimalmodbus
import serial
from .bus import Bus, bus_logger

SMARTSENSOR_MODBUS_ADDR = 0x01


class BusModbus(Bus):
    def __init__(self, bus_id, dev_addr):
        """
            Initialize Modbus bus with bus id and modbus slave address of the device
        :param bus_id: bus id (eg: '/dev/ttyUSB0')
        :param dev_addr: device address
        """
        super().__init__(Bus.Type.Modbus, dev_addr)
        self.bus = minimalmodbus.Instrument(bus_id, self.dev_addr)
        self.bus.serial.baudrate = 38400
        self.bus.serial.bytesize = 8
        self.bus.serial.parity = serial.PARITY_EVEN

    def read_register(self, reg_addr, bytes_cnt):
        """
            Read from modbus register with count in bytes
        :param reg_addr: modbus address
        :param bytes_cnt: count in bytes
        :return: bytes
        """
        num_reg = int((bytes_cnt + 1) / 2)
        data = self.bus.read_registers(reg_addr, num_reg)
        bus_logger.debug("Read 0x%04x <= %s" % (reg_addr, data))
        data_bytes = bytearray()
        for i in range(len(data)):
            data_bytes += bytearray([data[i] >> 8, data[i] & 0xff])
        return data_bytes

    def write_register(self, reg_addr, data):
        """
            Write to modbus register with data
        :param reg_addr: modbus address
        :param data: data in bytes
        """
        assert(type(data) is list)
        bus_logger.debug("Write 0x%04x => %s" % (reg_addr, data))
        num_reg = int((len(data) + 1) / 2)
        if len(data) % 2 == 1:
            data.append(0)
        values = [(data[2*i] << 8) + data[2*i+1] for i in range(num_reg)]
        self.bus.write_registers(reg_addr, values)
