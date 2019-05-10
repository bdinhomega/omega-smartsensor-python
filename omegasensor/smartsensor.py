import bitstruct, struct
import threading
import logging
from .bus import Bus
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

    @staticmethod
    def pack(data):
        assert(type(data) is ListSelect)
        return bitstruct.pack('>u8u8', data.list_select, data.block_select)

    @staticmethod
    def size():
        return 2


class _DataString32(_Serializer):
    @staticmethod
    def unpack(value):
        return bitstruct.unpack('t%d' % (__class__.size() * 8), value)[0].split('\0')[0]

    @staticmethod
    def pack(data):
        assert(type(data) is str)
        return bitstruct.pack('t%d' % (__class__.size() * 8), data + '\0')  # last char is null

    @staticmethod
    def size():
        return 32


class _DataUnit(_Serializer):
    @staticmethod
    def unpack(value):
        return ''.join([chr(i) for i in value]).split('\0')[0]

    @staticmethod
    def pack(data):
        assert(type(data) is str)
        bytes = [ord(c) for c in data][:__class__.size()]
        if len(bytes) < __class__.size():
            bytes.append(0)       # null terminated
        else:
            bytes[__class__.size()-1] = 0
        return bytearray(bytes)

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
        ret.device_type = SensorDevice(ret.device_type)
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
                              data.device_type.value,
                              )
    
    @staticmethod
    def size():
        return 4


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
    R.SENSOR_LIST_SELECT:       {"Modbus": 0xf006, "I2C": 0x0C,  "Access": _RW, "Data": _ListSelectSer},
    R.BLOCK_OPTIONS:            {"Modbus": 0xf006, "I2C": 0x0C,  "Access": _RW, "Data": _ListSelectSer},
    R.OPERATING_HOURS:          {"Modbus": 0xf007, "I2C": 0x0E,  "Access": _RW, "Data": _DataUInt16},
    R.EVENT_1_TIME_BASE:        {"Modbus": 0xf008, "I2C": 0x10,  "Access": _RW, "Data": _DataUInt16},
    R.EVENT_2_TIME_BASE:        {"Modbus": 0xf009, "I2C": 0x12,  "Access": _RW, "Data": _DataUInt16},
    R.SYSTEM_CONTROL:           {"Modbus": 0xf00a, "I2C": 0x14,  "Access": _RW, "Data": _DataUInt16},
    R.INTERRUPT_STATUS:         {"Modbus": 0xf00b, "I2C": 0x16,  "Access": _RW, "Data": _DataUInt16},
    R.INTERRUPT_CONTROL:        {"Modbus": 0xf00c, "I2C": 0x18,  "Access": _RW, "Data": _DataUInt16},
    R.NUMBER_OF_SENSORS:        {"Modbus": 0xf00d, "I2C": 0x1A,  "Access": _RO, "Data": _DataUInt16Lower},
    R.NUMBER_OF_OUTPUTS:        {"Modbus": 0xf00d, "I2C": 0x1A,  "Access": _RO, "Data": _DataUInt16Upper},
    R.OPERATING_TEMP:           {"Modbus": 0xf00e, "I2C": 0x1C,  "Access": _RO, "Data": _DataUInt16Lower},
    R.OPERATING_VOLTAGE:        {"Modbus": 0xf00e, "I2C": 0x1D,  "Access": _RO, "Data": _DataUInt16Upper},
    R.FAULT_PROCESS:            {"Modbus": 0xf00f, "I2C": 0x1E,  "Access": _RO, "Data": _DataUInt16Lower},
    R.FAULT_CODE:               {"Modbus": 0xf00f, "I2C": 0x1F,  "Access": _RO, "Data": _DataUInt16Upper},
    R.EVENT_1_TIMER:            {"Modbus": 0xf010, "I2C": 0x20,  "Access": _RO, "Data": _DataUInt16},
    R.EVENT_2_TIMER:            {"Modbus": 0xf011, "I2C": 0x22,  "Access": _RO, "Data": _DataUInt16},
    R.SYSTEM_STATUS:            {"Modbus": 0xf012, "I2C": 0x24,  "Access": _RO, "Data": _SystemStatusSer},
    R.TRIGGER_REQUESTS:         {"Modbus": 0xf013, "I2C": 0x26,  "Access": _RW, "Data": _DataUInt16}, # Trigger
    R.EXTRACT_I2C_TIME:         {"Modbus": 0xf014, "I2C": 0x28,  "Access": _RW, "Data": _DataUInt32},
    R.EXTRACT_END_TIME:         {"Modbus": 0xf015, "I2C": 0x2C,  "Access": _RW, "Data": _DataUInt32},
    R.NUMBER_OF_RECORDS:        {"Modbus": 0xf01b, "I2C": 0x36,  "Access": _RO, "Data": _DataUInt16},
    R.CURRENT_TIME:             {"Modbus": 0xf01c, "I2C": 0x38,  "Access": _RW, "Data": _DataTimeSer},

    R.SENSOR_1_DATA:            {"Modbus": 0xf01e, "I2C": 0x3C,  "Access": _RO, "Data": _DataFloat},
    R.SENSOR_2_DATA:            {"Modbus": 0xf020, "I2C": 0x40,  "Access": _RO, "Data": _DataFloat},
    R.SENSOR_3_DATA:            {"Modbus": 0xf022, "I2C": 0x44,  "Access": _RO, "Data": _DataFloat},
    R.SENSOR_4_DATA:            {"Modbus": 0xf024, "I2C": 0x48,  "Access": _RO, "Data": _DataFloat},
    R.EXTRACTED_TIME_STAMP:     {"Modbus": 0xf026, "I2C": 0x4C,  "Access": _RO, "Data": _DataUInt32},

    R.SENSOR_1_EXTRACTED_DATA:  {"Modbus": 0xf028, "I2C": 0x50,  "Access": _RO, "Data": _DataFloat},
    R.SENSOR_2_EXTRACTED_DATA:  {"Modbus": 0xf02a, "I2C": 0x54,  "Access": _RO, "Data": _DataFloat},
    R.SENSOR_3_EXTRACTED_DATA:  {"Modbus": 0xf02c, "I2C": 0x58,  "Access": _RO, "Data": _DataFloat},
    R.SENSOR_4_EXTRACTED_DATA:  {"Modbus": 0xf02e, "I2C": 0x5C,  "Access": _RO, "Data": _DataFloat},

    R.SENSOR_1_DESCRIPTOR:      {"Modbus": 0xf030, "I2C": 0x60, "Access": _RO, "Data": _SensorDescriptorSer},
    R.SENSOR_2_DESCRIPTOR:      {"Modbus": 0xf034, "I2C": 0x68, "Access": _RO, "Data": _SensorDescriptorSer},
    R.SENSOR_3_DESCRIPTOR:      {"Modbus": 0xf038, "I2C": 0x70, "Access": _RO, "Data": _SensorDescriptorSer},
    R.SENSOR_4_DESCRIPTOR:      {"Modbus": 0xf03c, "I2C": 0x78, "Access": _RO, "Data": _SensorDescriptorSer},

    R.SENSOR_1_GAIN:            {"Modbus": 0xf060, "I2C": 0xC0, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_2_GAIN:            {"Modbus": 0xf064, "I2C": 0xC8, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_3_GAIN:            {"Modbus": 0xf068, "I2C": 0xD0, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_4_GAIN:            {"Modbus": 0xf06c, "I2C": 0xD8, "Access": _RW, "Data": _DataFloat},

    R.SENSOR_1_OFFSET:          {"Modbus": 0xf062, "I2C": 0xC4, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_2_OFFSET:          {"Modbus": 0xf066, "I2C": 0xCC, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_3_OFFSET:          {"Modbus": 0xf06a, "I2C": 0xD4, "Access": _RW, "Data": _DataFloat},
    R.SENSOR_4_OFFSET:          {"Modbus": 0xf06e, "I2C": 0xDC, "Access": _RW, "Data": _DataFloat},


    R.SENSOR_1_UNIT:            {"Modbus": 0xf032, "I2C": 0x64, "Access": _RW, "Data": _DataUnit},
    R.SENSOR_2_UNIT:            {"Modbus": 0xf036, "I2C": 0x6C, "Access": _RW, "Data": _DataUnit},
    R.SENSOR_3_UNIT:            {"Modbus": 0xf03a, "I2C": 0x74, "Access": _RW, "Data": _DataUnit},
    R.SENSOR_4_UNIT:            {"Modbus": 0xf03e, "I2C": 0x7C, "Access": _RW, "Data": _DataUnit},

    R.DEVICE_NAME:              {"Modbus": 0xf070, "I2C": 0xE0,  "Access": _RW, "Data": _DataString32},
    R.OUTPUT_1:                 {"Modbus": 0xf078, "I2C": 0xF0,  "Access": _RW, "Data": _DataFloat},
    R.OUTPUT_2:                 {"Modbus": 0xf07a, "I2C": 0xF4,  "Access": _RW, "Data": _DataFloat},
    R.OUTPUT_3:                 {"Modbus": 0xf07c, "I2C": 0xF8,  "Access": _RW, "Data": _DataFloat},
    R.OUTPUT_4:                 {"Modbus": 0xf07e, "I2C": 0xFC,  "Access": _RW, "Data": _DataFloat},

    # Manufacturing registers / May Require Unlock
    R.MFR_DEVICE_ID:            {"Modbus": 0xf080,  'I2C': 0x100, "Access": _PR, "Data": _DataUInt32},
    R.MFR_HARDWARE_VERSION:     {"Modbus": 0xf082,  'I2C': 0x104, "Access": _PR, "Data": _DataUInt32},
    R.MFR_CORE_FIRMWARE_VER:    {"Modbus": 0xf084,  'I2C': 0x108, "Access": _PR, "Data": _DataUInt32},
    R.MFR_BLOCK_I2C_RETRY:      {"Modbus": 0xf086,  'I2C': 0x10c, "Access": _PR, "Data": _DataUInt16},
    R.MFR_RTC_CALIBRATION:      {"Modbus": 0xf087,  'I2C': 0x10e, "Access": _PR, "Data": _DataUInt16},
    R.MFR_FEATURE_BITS:         {"Modbus": 0xf088,  'I2C': 0x110, "Access": _PR, "Data": _DataUInt32},
    R.MFR_DEFAULT_EVENT_1_TIME_BASE: {"Modbus": 0xf08a,  'I2C': 0x114, "Access": _PR, "Data": _DataUInt16},
    R.MFR_DEFAULT_EVENT_2_TIME_BASE: {"Modbus": 0xf08b,  'I2C': 0x116, "Access": _PR, "Data": _DataUInt16},
    R.MFR_SYSTEM_CONTROL:       {"Modbus": 0xf08c,  'I2C': 0x118, "Access": _PR, "Data": _DataUInt16},
    R.MFR_SYSTEM_INTERRUPT:     {"Modbus": 0xf08d,  'I2C': 0x11a, "Access": _PR, "Data": _DataUInt16},
    R.MFR_SENSOR_LIST_INDEX:    {"Modbus": 0xf08e,  'I2C': 0x11c, "Access": _PR, "Data": _DataUInt16},
    R.MFR_SENSOR_LIST_SELECT:   {"Modbus": 0xf08f,  'I2C': 0x11e, "Access": _PR, "Data": _DataUInt16},
    R.MFR_ERROR_COUNT_1:        {"Modbus": 0xf090,  'I2C': 0x120, "Access": _PR, "Data": _DataUInt16},
    R.MFR_ERROR_COUNT_2:        {"Modbus": 0xf091,  'I2C': 0x122, "Access": _PR, "Data": _DataUInt16},
    R.MFR_ERROR_COUNT_3:        {"Modbus": 0xf092,  'I2C': 0x124, "Access": _PR, "Data": _DataUInt16},
    R.MFR_ERROR_COUNT_4:        {"Modbus": 0xf093,  'I2C': 0x126, "Access": _PR, "Data": _DataUInt16},
    R.MFR_MANUFACTURING_DATE:   {"Modbus": 0xf094,  'I2C': 0x128, "Access": _PR, "Data": _DataUInt16},
    R.MFR_CALIBRATION_DATE:     {"Modbus": 0xf095,  'I2C': 0x12a, "Access": _PR, "Data": _DataUInt16},
    R.MFR_OPERATING_TIME:       {"Modbus": 0xf096,  'I2C': 0x12c, "Access": _PR, "Data": _DataUInt32},
    R.MFR_CALIBRATION_TIME:     {"Modbus": 0xf098,  'I2C': 0x12e, "Access": _PR, "Data": _DataUInt32},
    R.MFR_OUTPUT_CONFIG_1:      {"Modbus": 0xf09a,  'I2C': 0x130, "Access": _PR, "Data": _DataUInt16},
    R.MFR_OUTPUT_CONFIG_2:      {"Modbus": 0xf09b,  'I2C': 0x132, "Access": _PR, "Data": _DataUInt16},
    R.MFR_OUTPUT_CONFIG_3:      {"Modbus": 0xf09c,  'I2C': 0x134, "Access": _PR, "Data": _DataUInt16},
    R.MFR_OUTPUT_CONFIG_4:      {"Modbus": 0xf09d,  'I2C': 0x136, "Access": _PR, "Data": _DataUInt16},


    R.MFR_MSP430_CL_1:          {"Modbus": 0xf100,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_MSP430_CL_2:          {"Modbus": 0xf108,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_MSP430_V1_1:          {"Modbus": 0xf110,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_MSP430_V1_2:          {"Modbus": 0xf118,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_CL_1:         {"Modbus": 0xf120,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_CL_2:         {"Modbus": 0xf128,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_V1_1:         {"Modbus": 0xf130,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_V1_2:         {"Modbus": 0xf138,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_P1_1:         {"Modbus": 0xf140,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_P1_2:         {"Modbus": 0xf148,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_P05_1:        {"Modbus": 0xf150,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_P05_2:        {"Modbus": 0xf158,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_V10_1:        {"Modbus": 0xf160,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS1248_V10_2:        {"Modbus": 0xf168,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS_TC_1:             {"Modbus": 0xf170,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS_TC_2:             {"Modbus": 0xf178,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS_RTD_2W:           {"Modbus": 0xf188,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS_RTD_3W:           {"Modbus": 0xf190,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
    R.MFR_ADS_RTD_4W:           {"Modbus": 0xf198,  'I2C': None, "Access": _PR, "Data": _CalibrationSer},
}

api_logger = logging.getLogger('[API]')
api_logger.setLevel(logging.INFO)


class Device:
    def __init__(self, transport: Bus):
        """
            Initialize smartsensor device
        :param transport: communication bus
        """
        self.trans = transport
        self.lock = threading.Lock()
        self._debug = False

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
