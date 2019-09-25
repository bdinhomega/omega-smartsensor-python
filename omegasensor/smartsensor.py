import bitstruct, struct
import threading
import logging
from .bus import Bus
from sys import platform
if platform != "win32": #do not import rasberry pi library for windows
    from .interrupt import *
from .registers import *


class _Serializer:
    @staticmethod
    def pack(value):      # to bytes
        raise NotImplemented

    @staticmethod
    def unpack(value):    # from bytes
        raise NotImplemented

    @staticmethod
    def size():
        raise NotImplemented


class _DataUInt32(_Serializer):
    @staticmethod
    def unpack(value):
        return struct.unpack('>I', value)[0]

    @staticmethod
    def pack(value):
        return struct.pack('>I', value)

    @staticmethod
    def size():
        return 4


class _DataUInt16(_Serializer):
    @staticmethod
    def unpack(value):
        return struct.unpack('>H', value)[0]

    @staticmethod
    def pack(value):
        if isinstance(value, Enum):
            value = value.value
        return struct.pack('>H', value)

    @staticmethod
    def size():
        return 2


class _DataUInt16Upper(_Serializer):
    @staticmethod
    def unpack(value):
        return bitstruct.unpack('>u8u8', value)[1]

    @staticmethod
    def pack(value):
        if isinstance(value, Enum):
            value = value.value
        return bitstruct.pack('>u8u8', value)

    @staticmethod
    def size():
        return 2


class _DataUInt16Lower(_Serializer):
    @staticmethod
    def unpack(value):
        return bitstruct.unpack('>u8u8', value)[0]

    @staticmethod
    def pack(value):
        if isinstance(value, Enum):
            value = value.value
        return bitstruct.pack('>u8u8', value)

    @staticmethod
    def size():
        return 2


class _DataFloat(_Serializer):
    @staticmethod
    def unpack(value):
        return struct.unpack('>f', value)[0]

    @staticmethod
    def pack(value):
        return struct.pack('>f', value)

    @staticmethod
    def size():
        return 4


class _ListSelectSer(_Serializer):
    @staticmethod
    def unpack(data):
        ret = ListSelect()
        ret.list_select, ret.block_select = bitstruct.unpack('>u8u8', data)
        return ret

    @staticmethod
    def pack(data):
        assert(type(data) is ListSelect)
        return bitstruct.pack('>u8u8', data.list_select, data.block_select)

    @staticmethod
    def size():
        return 2


class _DataFaultParam(_Serializer):
    @staticmethod
    def unpack(data):
        ret = FaultParam()
        ret.fault_process, ret.fault_code = bitstruct.unpack('>u8u8', data)
        return ret

    @staticmethod
    def pack(data):
        assert (type(data) is FaultParam)
        return bitstruct.pack('>u8u8', data.fault_process, data.fault_code)

    @staticmethod
    def size():
        return 2


class _DataOperatingParam(_Serializer):
    @staticmethod
    def unpack(data):
        ret = OperatingParam()
        ret.operating_temp, ret.operating_voltage = bitstruct.unpack('>u8u8', data)
        return ret

    @staticmethod
    def pack(data):
        assert (type(data) is OperatingParam)
        return bitstruct.pack('>u8u8', data.operating_temp, data.operating_voltage)

    @staticmethod
    def size():
        return 2


class _DataIoCount(_Serializer):
    @staticmethod
    def unpack(data):
        ret = IoCount()
        ret.sensors, ret.outputs = bitstruct.unpack('>u8u8', data)
        return ret

    @staticmethod
    def pack(data):
        assert (type(data) is IoCount)
        return bitstruct.pack('>u8u8', data.num_of_sensors, data.num_of_outputs)

    @staticmethod
    def size():
        return 2


class _StringSerializer(_Serializer):
    @staticmethod
    def unpack(value):
        return ''.join([chr(i) for i in value]).split('\0')[0]

    @staticmethod
    def pack_with_size(data, size):
        assert (type(data) is str)
        bytes = [ord(c) for c in data][:size]
        if len(bytes) < size:
            bytes.append(0)  # null terminated
        return bytearray(bytes)


class _DataString32(_StringSerializer):
    @staticmethod
    def pack(data):
        return _StringSerializer.pack_with_size(data, __class__.size())

    @staticmethod
    def size():
        return 32


class _DataDeviceNameList(_StringSerializer):
    @staticmethod
    def pack(data):
        return _StringSerializer.pack_with_size(data, __class__.size())

    @staticmethod
    def size():
        return 192


class _DataUnit(_StringSerializer):
    @staticmethod
    def pack(data):
        return _StringSerializer.pack_with_size(data, __class__.size())

    @staticmethod
    def size():
        return 4


class _CalibrationSer(_Serializer):
    @staticmethod
    def unpack(value):
        ret = Calibration()
        [
            ret.active_segment,
            ret.max_segment,
            ret.polynomial_order,
            ret.max_polynomial,
            ret.inflection_point,
            ret.offset,
            ret.gain] = bitstruct.unpack('u8u8u8u8f32f32f32', value)
        return ret

    @staticmethod
    def pack(data):
        assert(type(data) is Calibration)
        return bitstruct.pack('u8u8u8u8f32f32f32',
                              data.active_segment,
                              data.max_segment,
                              data.polynomial_order,
                              data.max_polynomial,
                              data.inflection_point,
                              data.offset,
                              data.gain)

    @staticmethod
    def size():
        return 16


class _SensorDescriptorSer(_Serializer):
    @staticmethod
    def unpack(value):
        ret = SensorDescriptor()
        [
            ret.meas_type,
            ret.data_extended_function,
            ret.data_factory_calibrate,
            ret.data_config_descriptor,
            ret.data_smartsensor,
            ret.data_type,
            ret.config_lock,
            ret.config_scaling,
            ret.config_assigned_channel,
            ret.config_available,
            ret.config_sensor_type,
            ret.device_type,
        ] = bitstruct.unpack('u8b1b1b1b1u4b1b1b1b1u4u8', value)
        ret.meas_type = MeasurementType(ret.meas_type)
        ret.data_type = DataType(ret.data_type)
        return ret

    @staticmethod
    def pack(data):
        assert(type(data) is SensorDescriptor)
        return bitstruct.pack('u8b1b1b1b1u4b1b1b1b1u4u8',
                              data.meas_type.value,
                              data.data_extended_function,
                              data.data_factory_calibrate,
                              data.data_config_descriptor,
                              data.data_smartsensor,
                              data.data_type.value,
                              data.config_lock,
                              data.config_scaling,
                              data.config_assigned_channel,
                              data.config_available,
                              data.config_sensor_type.value,
                              data.device_type,
                              )
    
    @staticmethod
    def size():
        return 4


class DeviceType(_Serializer):
    @staticmethod
    def unpack(value):
        value = bytes([value]) #need to cast as byte
        ret = DigitalInputDeviceByte()
        [
            ret.extra_bit,
            ret.enable,
            ret.reset,
            ret.clock
        ] = bitstruct.unpack('b1u2u2u3', value)
        return ret

    @staticmethod
    def pack(data):
        """Put back the bits together into a format accepted by device_type in sensor descriptor

        :param data: modified DigitalInputDeviceByte
        :return: value for device_type in sensordescriptor
        """
        assert(type(data) is DigitalInputDeviceByte)
        value = bitstruct.pack('b1u2u2u3',
                               data.extra_bit,
                               data.enable,
                               data.reset,
                               data.clock)
        value = int.from_bytes(value, 'little')
        return value
    @staticmethod
    def size():
        return 1


class _SystemStatusSer(_Serializer):
    @staticmethod
    def unpack(value):
        ret = SystemStatus()
        [
            ret.device_locked,
            ret.factory_access,
            ret.device_ready,
            ret.health_fault,
            ret.sensor_fault,
            ret.read_active,
            ret.extract_valid,
            ret.sensor_valid,
            ret.system_fault,
            ret.intr_active,
            ret.device_reset,
            ret.power_reset,
            ret.sensor_bits,
        ] = bitstruct.unpack('b1b1b1b1b1b1b1b1b1b1b1b1u4', value)
        return ret

    @staticmethod
    def pack(data):
        assert(type(data) is SystemStatus)
        return bitstruct.pack('b1b1b1b1b1b1b1b1b1b1b1b1u4',
                              data.device_locked,
                              data.factory_access,
                              data.device_ready,
                              data.health_fault,
                              data.sensor_fault,
                              data.read_active,
                              data.extract_valid,
                              data.sensor_valid,
                              data.system_fault,
                              data.intr_active,
                              data.device_reset,
                              data.power_reset,
                              data.sensor_bits,
                              )

    @staticmethod
    def size():
        return 2


class _DataTimeSer(_Serializer):
    @staticmethod
    def pack(data):
        assert(type(data) is DataTime)
        return data.days * 24 * 3600 \
                + data.hours * 3600  \
                + data.mins * 60     \
                + data.secs

    @staticmethod
    def unpack(data):
        value, = struct.unpack('>I', data)
        ret = DataTime()
        ret.secs = value % 60
        value /= 60
        ret.mins = int(value) % 60
        value /= 60
        ret.hours = int(value) % 24
        ret.days = int(value / 24)
        return ret

    @staticmethod
    def size():
        return 4

_RO = 0  # read only
_RW = 1
_PR = 3  # protected

_def = {
    R.DEVICE_ID:                {"Modbus": 0xf000, "I2C": 0x00,  "Access": _RO, "Data": _DataUInt32},
    R.FIRMARE_VERSION:          {"Modbus": 0xf002, "I2C": 0x04,  "Access": _RO, "Data": _DataUInt32},
    R.HARDWARE_VERSION:         {"Modbus": 0xf004, "I2C": 0x08,  "Access": _RO, "Data": _DataUInt32},
    R.LIST_INDEX_BLOCK_SELECT:  {"Modbus": 0xf006, "I2C": 0x0C, "Access": _RW, "Data": _ListSelectSer},
    R.USER_HOURS:               {"Modbus": 0xf007, "I2C": 0x0E, "Access": _RW, "Data": _DataUInt16},
    R.EVENT_0_TIME_BASE:        {"Modbus": 0xf008, "I2C": 0x10, "Access": _RW, "Data": _DataUInt16},
    R.EVENT_1_TIME_BASE:        {"Modbus": 0xf009, "I2C": 0x12, "Access": _RW, "Data": _DataUInt16},
    R.SYSTEM_CONTROL:           {"Modbus": 0xf00a, "I2C": 0x14,  "Access": _RW, "Data": _DataUInt16},
    R.INTERRUPT_STATUS:         {"Modbus": 0xf00b, "I2C": 0x16,  "Access": _RW, "Data": _DataUInt16},
    R.INTERRUPT_CONTROL:        {"Modbus": 0xf00c, "I2C": 0x18,  "Access": _RW, "Data": _DataUInt16},
    R.IO_COUNT:                 {"Modbus": 0xf00d, "I2C": 0x1A,  "Access": _RO, "Data": _DataIoCount},
    R.OPERATING_PARAM:          {"Modbus": 0xf00e, "I2C": 0x1C, "Access": _RO, "Data": _DataOperatingParam},
    R.FAULT_PARAM:              {"Modbus": 0xf00f, "I2C": 0x1E, "Access": _RO, "Data": _DataFaultParam},
    R.EVENT_0_TIMER:            {"Modbus": 0xf010, "I2C": 0x20, "Access": _RW, "Data": _DataUInt16},
    R.EVENT_1_TIMER:            {"Modbus": 0xf011, "I2C": 0x22, "Access": _RW, "Data": _DataUInt16},
    R.SYSTEM_STATUS:            {"Modbus": 0xf012, "I2C": 0x24,  "Access": _RO, "Data": _SystemStatusSer},
    R.TRIGGER_REQUESTS:         {"Modbus": 0xf013, "I2C": 0x26,  "Access": _RW, "Data": _DataUInt16}, # Trigger
    R.EXTRACT_START_TIME:       {"Modbus": 0xf014, "I2C": 0x28, "Access": _RW, "Data": _DataUInt32},
    R.EXTRACT_END_TIME:         {"Modbus": 0xf015, "I2C": 0x2C,  "Access": _RW, "Data": _DataUInt32},
    R.NUMBER_OF_RECORDS:        {"Modbus": 0xf01b, "I2C": 0x36,  "Access": _RO, "Data": _DataUInt16},
    R.CURRENT_TIME:             {"Modbus": 0xf01c, "I2C": 0x38,  "Access": _RW, "Data": _DataTimeSer},

    R.SENSOR_0_DATA:            {"Modbus": 0xf01e, "I2C": 0x3C, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_1_DATA:            {"Modbus": 0xf020, "I2C": 0x40, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_2_DATA:            {"Modbus": 0xf022, "I2C": 0x44, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_3_DATA:            {"Modbus": 0xf024, "I2C": 0x48, "Access": _RW, "Data": _DataFloat},
    R.EXTRACTED_TIME_STAMP:     {"Modbus": 0xf026, "I2C": 0x4C,  "Access": _RO, "Data": _DataUInt32},

    R.EXTRACTED_DATA_0:         {"Modbus": 0xf028, "I2C": 0x50, "Access": _RO, "Data": _DataFloat},
    R.EXTRACTED_DATA_1:         {"Modbus": 0xf02a, "I2C": 0x54, "Access": _RO, "Data": _DataFloat},
    R.EXTRACTED_DATA_2:         {"Modbus": 0xf02c, "I2C": 0x58, "Access": _RO, "Data": _DataFloat},
    R.EXTRACTED_DATA_3:         {"Modbus": 0xf02e, "I2C": 0x5C, "Access": _RO, "Data": _DataFloat},

    R.SENSOR_0_DESCRIPTOR:      {"Modbus": 0xf030, "I2C": 0x60, "Access": _RW, "Data": _SensorDescriptorSer},
    R.SENSOR_1_DESCRIPTOR:      {"Modbus": 0xf034, "I2C": 0x68, "Access": _RW, "Data": _SensorDescriptorSer},
    R.SENSOR_2_DESCRIPTOR:      {"Modbus": 0xf038, "I2C": 0x70, "Access": _RW, "Data": _SensorDescriptorSer},
    R.SENSOR_3_DESCRIPTOR:      {"Modbus": 0xf03c, "I2C": 0x78, "Access": _RW, "Data": _SensorDescriptorSer},

    R.SENSOR_0_GAIN:            {"Modbus": 0xf060, "I2C": 0xC0, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_1_GAIN:            {"Modbus": 0xf064, "I2C": 0xC8, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_2_GAIN:            {"Modbus": 0xf068, "I2C": 0xD0, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_3_GAIN:            {"Modbus": 0xf06c, "I2C": 0xD8, "Access": _RW, "Data": _DataFloat},

    R.SENSOR_0_OFFSET:          {"Modbus": 0xf062, "I2C": 0xC4, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_1_OFFSET:          {"Modbus": 0xf066, "I2C": 0xCC, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_2_OFFSET:          {"Modbus": 0xf06a, "I2C": 0xD4, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_3_OFFSET:          {"Modbus": 0xf06e, "I2C": 0xDC, "Access": _RW, "Data": _DataFloat},


    R.SENSOR_0_UNIT:            {"Modbus": 0xf032, "I2C": 0x64, "Access": _RW, "Data": _DataUnit},
    R.SENSOR_1_UNIT:            {"Modbus": 0xf036, "I2C": 0x6C, "Access": _RW, "Data": _DataUnit},
    R.SENSOR_2_UNIT:            {"Modbus": 0xf03a, "I2C": 0x74, "Access": _RW, "Data": _DataUnit},
    R.SENSOR_3_UNIT:            {"Modbus": 0xf03e, "I2C": 0x7C, "Access": _RW, "Data": _DataUnit},

    R.DEVICE_NAME:              {"Modbus": 0xf070, "I2C": 0xE0, "Access": _RW, "Data": _DataString32},
    R.OUTPUT_0:                 {"Modbus": 0xf078, "I2C": 0xF0, "Access": _RW, "Data": _DataFloat},
    R.OUTPUT_1:                 {"Modbus": 0xf07a, "I2C": 0xF4, "Access": _RW, "Data": _DataFloat},
    R.OUTPUT_2:                 {"Modbus": 0xf07c, "I2C": 0xF8, "Access": _RW, "Data": _DataFloat},
    R.OUTPUT_3:                 {"Modbus": 0xf07e, "I2C": 0xFC, "Access": _RW, "Data": _DataFloat},

    # Manufacturing registers
    R.LONG_DEVICE_ID:           {"Modbus": 0xf080, 'I2C': 0x100, "Access": _RO, "Data": _DataUInt32},
    R.CORE_VERSION:             {"Modbus": 0xf084, 'I2C': 0x108, "Access": _RO, "Data": _DataUInt32},
    R.BLOCK_START_RETRY_COUNT:  {"Modbus": 0xf086, 'I2C': 0x10c, "Access": _RO, "Data": _DataUInt16},
    R.RTC_CALIBRATION_CONTROL:  {"Modbus": 0xf087, 'I2C': 0x10e, "Access": _RO, "Data": _DataUInt16},
    R.FEATURE_BITS:             {"Modbus": 0xf088, 'I2C': 0x110, "Access": _RO, "Data": _DataUInt32},
    R.DEFAULT_EVENT_0_TIME_BASE:{"Modbus": 0xf08a, 'I2C': 0x114, "Access": _RO, "Data": _DataUInt16},
    R.DEFAULT_EVENT_1_TIME_BASE:{"Modbus": 0xf08b, 'I2C': 0x116, "Access": _RO, "Data": _DataUInt16},
    R.DEFAULT_SYSTEM_CONTROL:   {"Modbus": 0xf08c, 'I2C': 0x118, "Access": _RO, "Data": _DataUInt16},
    R.DEFAULT_INTERRUPT_CONTROL:{"Modbus": 0xf08d, 'I2C': 0x11a, "Access": _RO, "Data": _DataUInt16},
    R.SENSOR_LIST_INDEX:        {"Modbus": 0xf08e, 'I2C': 0x11c, "Access": _RO, "Data": _DataUInt16},
    R.SENSOR_LIST_SELECT:       {"Modbus": 0xf08f, 'I2C': 0x11e, "Access": _RO, "Data": _DataUInt16},
    R.SENSOR_0_ERROR_COUNT:     {"Modbus": 0xf090, 'I2C': 0x120, "Access": _RO, "Data": _DataUInt16},
    R.SENSOR_1_ERROR_COUNT:     {"Modbus": 0xf091, 'I2C': 0x122, "Access": _RO, "Data": _DataUInt16},
    R.SENSOR_2_ERROR_COUNT:     {"Modbus": 0xf092, 'I2C': 0x124, "Access": _RO, "Data": _DataUInt16},
    R.SENSOR_3_ERROR_COUNT:     {"Modbus": 0xf093, 'I2C': 0x126, "Access": _RO, "Data": _DataUInt16},
    R.MANUFACTURED_DATE:        {"Modbus": 0xf094, 'I2C': 0x128, "Access": _RO, "Data": _DataUInt16},
    R.CALIBRATION_DATE:         {"Modbus": 0xf095, 'I2C': 0x12a, "Access": _RO, "Data": _DataUInt16},
    R.OPERATING_TIME:           {"Modbus": 0xf096, 'I2C': 0x12c, "Access": _RO, "Data": _DataUInt32},
    R.CALIBRATION_TIME:         {"Modbus": 0xf098, 'I2C': 0x12e, "Access": _RO, "Data": _DataUInt32},
    R.OUTPUT_0_CONFIG:          {"Modbus": 0xf09a, 'I2C': 0x130, "Access": _RO, "Data": _DataUInt16},
    R.OUTPUT_1_CONFIG:          {"Modbus": 0xf09b, 'I2C': 0x132, "Access": _RO, "Data": _DataUInt16},
    R.OUTPUT_2_CONFIG:          {"Modbus": 0xf09c, 'I2C': 0x134, "Access": _RO, "Data": _DataUInt16},
    R.OUTPUT_3_CONFIG:          {"Modbus": 0xf09d, 'I2C': 0x136, "Access": _RO, "Data": _DataUInt16},
    R.BASE_HARDWARE_TYPE:       {"Modbus": 0xf09e, 'I2C': 0x13c, "Access": _RO, "Data": _DataUInt16},
    R.EXTRACT_STOP_SIZE:        {"Modbus": 0xf09f, 'I2C': 0x13e, "Access": _RO, "Data": _DataUInt16},
    R.DEVICE_NAME_LIST:         {"Modbus": 0xf0a0, 'I2C': 0x140, "Access": _RO, "Data": _DataDeviceNameList},

}

api_logger = logging.getLogger('[API]')
api_logger.setLevel(logging.INFO)

DEFAULT_HEARTBEAT_MAX_MISS  = 3

## module global for inferring interrupt to corresponding object and its handler
module_instances = []

class Device:
    def __init__(self,
                 transport: Bus,
                 interrupt_pin: int = None,
                 interrupt_callback = None,
                 config: dict = {}):
        """
            Initialize smartsensor device
        :param transport: communication bus
        """
        self.trans = transport
        self.lock = threading.Lock()
        self._debug = False
        self.intr_pin = None
        self.sensor_attached = False
        self.heartbeat_miss = 0
        self.heartbeat_max_miss = config.get('HEARTBEAT_MAX_MISS', DEFAULT_HEARTBEAT_MAX_MISS)
        if interrupt_pin and interrupt_callback:
            self.intr_pin = interrupt_pin
            self.user_callback = interrupt_callback
            setup_interrupt(interrupt_pin, self.interrupt_handler)
        module_instances.append(self)

    def __del__(self):
        """
            Executes when the instance goes out of scope
        :return:
        """
        if self.intr_pin:
            remove_interrupt(self.intr_pin)
        module_instances.remove(self)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value
        if value:
            api_logger.setLevel(logging.DEBUG)
        else:
            api_logger.setLevel(logging.INFO)

    @staticmethod
    def interrupt_handler(pin):
        for instance in module_instances:
            if instance.intr_pin == pin:
                instance.handle_interrupt()

    def handle_interrupt(self) -> None:
        """
            Handle logic when an interrupt is raised from the smartsensor
        :return: None
        """
        if self.sensor_attached:
            try:
                intr_status = self.read(R.INTERRUPT_STATUS)
                # alert user of the interrupt status
                api_event = ApiEvent(intr_status)
                self.user_callback(api_event)
            except:
                # failed to communicate
                self.heartbeat_miss += 1
                if self.heartbeat_miss > self.heartbeat_max_miss:
                    self.sensor_attached = False
                    api_event = ApiEvent.API_SENSOR_DETACHED
                    self.user_callback(api_event)
        else:
            try:
                sys_status = self.read(R.SYSTEM_STATUS)
                if sys_status.device_ready:
                    self.probe_init()
                    self.sensor_attached = True
                    self.heartbeat_miss = 0
                    api_event = ApiEvent.API_SENSOR_ATTACHED
                    self.user_callback(api_event)
            except:
                pass

    def timeout_handler(self) -> None:
        """
            Handle logic when a heartbeat timeout is lapsed
        :return:
        """
        pass

    def probe_init(self):
        intr_ctrl = self.read(R.INTERRUPT_CONTROL)
        intr_ctrl |=    InterruptEnable.INTR_SENSOR_CHANGE |\
                        InterruptEnable.INTR_POWER_CHANGE |\
                        InterruptEnable.INTR_HEALTH_CHANGE |\
                        InterruptEnable.INTR_DATA_READY |\
                        InterruptEnable.INTR_FUNCTION_BLOCK |\
                        InterruptEnable.INTR_LOG_DATA_READY
        self.write(R.INTERRUPT_CONTROL, intr_ctrl)

        sys_ctrl = self.read(R.SYSTEM_CONTROL)
        sys_ctrl |= SystemControl.ENABLE_SENSOR_CHANGE_LOG | \
                    SystemControl.ENABLE_POWER_CHANGE_LOG | \
                    SystemControl.ENABLE_HEALTH_FAULT_LOG | \
                    SystemControl.ENABLE_TIME_CHANGE_LOG | \
                    SystemControl.ENABLE_EVENT_0_READ | \
                    SystemControl.ENABLE_EVENT_0_LOG | \
                    SystemControl.ENABLE_FUNCTION_BLOCK | \
                    SystemControl.ENABLE_HEALTH_MONITOR | \
                    SystemControl.ENABLE_LOG_OVERWRITE | \
                    SystemControl.ENABLE_RTC
        self.write(R.SYSTEM_CONTROL, sys_ctrl)

        self.write(R.EXTRACT_START_TIME, 0)
        self.write(R.EXTRACT_END_TIME, 0xffffffff)

    def read(self, register: R):
        """
            Read from smartsensor register
        :param register: smart sensor register
        :return: data
        """
        reg_addr = _def[register]["Modbus"] if self.trans.bus_type == Bus.Type.Modbus else _def[register]["I2C"]
        assert reg_addr is not None
        handler = _def[register]["Data"]()
        with self.lock:
            data = self.trans.read_register(reg_addr, handler.size())

        api_logger.debug("Read  %20s <= %s" % (register.name, data))
        response = handler.unpack(bytearray(data))  # deserialize, cast
        return response

    def write(self, register: R, value):
        """
            Write to smartsensor register
        :param register: smart sensor register
        :param value: value
        """
        if _def[register]["Access"] in [_RO, _PR]:
            raise Exception("Register is read-only.")
        reg_addr = _def[register]["Modbus"] if self.trans.bus_type == Bus.Type.Modbus else _def[register]["I2C"]
        assert reg_addr
        api_logger.debug('Write %20s => %s' % (register.name, value))

        handler = _def[register]["Data"]()
        data = handler.pack(value)        # serialize to bytes
        with self.lock:
            self.trans.write_register(reg_addr, list(data))
