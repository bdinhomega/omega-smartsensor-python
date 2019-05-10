from enum import Enum


MAX_SENSOR_COUNT = 4


class _IntFlag(int, Enum):
    """
        Limited Support for IntFlag enumeration for Python < 3.6
    """
    def __or__(self, other):
        if not isinstance(other, (self.__class__, int)):
            return NotImplemented
        value = self.value | other._value_
        return value

    def __and__(self, other):
        if not isinstance(other, (self.__class__, int)):
            return NotImplemented
        return self.__class__(self._value_ & self.__class__(other)._value_)

    def __xor__(self, other):
        if not isinstance(other, (self.__class__, int)):
            return NotImplemented
        return self.__class__(self._value_ ^ self.__class__(other)._value_)

    def __invert__(self):
        result = self.__class__(~self._value_)
        return result

    def __repr__(self):
        return self.value


class SystemControl(_IntFlag):
    ENABLE_SENSOR_CHANGE_LOG = 1 << 0
    ENABLE_POWER_CHANGE_LOG = 1 << 1
    ENABLE_HEALTH_FAULT_LOG = 1 << 2
    ENABLE_TIME_CHANGE_LOG = 1 << 3
    ENABLE_EVENT_1_READ = 1 << 4
    ENABLE_EVENT_1_LOG = 1 << 5
    ENABLE_EVENT_2_READ = 1 << 6
    ENABLE_EVENT_2_LOG = 1 << 7
    ENABLE_EXTN_READ = 1 << 8
    ENABLE_EXTN_LOG = 1 << 9
    ENABLE_EXTN_RESET_EVENT_1 = 1 << 10
    ENABLE_EXTN_RESET_EVENT_2 = 1 << 11
    ENABLE_FUNCTION_BLOCK = 1 << 12
    ENABLE_HEALTH_MONITOR = 1 << 13
    ENABLE_LOG_OVERWRITE = 1 << 14
    ENABLE_RTC = 1 << 15


class InterruptSource(_IntFlag):
    SENSOR_CHANGE_INTR = 0x0001
    POWER_CHANGE_INTR = 0x0002
    HEALTH_CHANGE_INTR = 0x0004
    EVENT_1_INTR = 0x0008
    EVENT_2_INTR = 0x0010
    DATA_INVALID_INTR = 0x0020
    FUNTION_BLOCK_INTR = 0x0040


class InterruptEnable(_IntFlag):
    INTR_SENSOR_CHANGE = 1 << 0
    INTR_POWER_CHANGE = 1 << 1
    INTR_HEALTH_CHANGE = 1 << 2
    INTR_EVENT_1 = 1 << 3
    INTR_EVENT_2 = 1 << 4
    INTR_DATA_READY = 1 << 5
    INTR_FUNCTION_ALARM = 1 << 6
    INTR_LOG_DATA_READY = 1 << 7


class MeasurementType(Enum):
    Error = 0
    Temperature_C = 0x01
    Humidity_TH_percent = 0x02
    Pressure_mbar = 0x03
    Light_lx = 0x04
    ProcessVoltage_V = 0x10
    ProcessVoltage_mV = 0x11
    ProcessCurrent_A = 0x12
    ProcessCurrent_mA = 0x13
    DioType = 0x17
    DigitalInput = 0x18
    Frequency_hz = 0x19
    PulseWidth_sec = 0x1a
    PulseDelay_sec = 0x1b
    DutyCycle_percent = 0x1c
    Count_count = 0x1d
    UpDownCount_count = 0x1e
    QuadCount_count = 0x1f

    Thermocouple_C = 0x20
    RTD_C = 0x21
    Thermistor_C = 0x22
    Infrared_C = 0x23
    CJC_C = 0x24
    PH = 0x25
    CO2 = 0x26

    Bridge = 0x27
    Pressure = 0x28
    Acceleration = 0x29
    Inclination = 0x2a
    Serial = 0x30
    AdcCount = 0x31


class SensorDevice(Enum):
    NULL = 0
    FILES = 1
    ADC = 2
    SHT75 = 3
    TMP275 = 4
    MS8607 = 5
    TSL4531 = 6
    MS5534 = 7
    MLX = 8
    UNKNOWN_1 = 15
    BUG = 210
    BUG_2 = 128
    BUG_3 = 208


class Trigger(_IntFlag):
    UNKNOWN                 = 0x0000
    EXTRACT_RECORD          = 0x0001
    EXTRACT_NEXT            = 0x0002
    CLEAR_LOG               = 0x0003

    DEVICE_RESET            = 0x0004
    FACTORY_RESET           = 0x0005
    POWER_RESET             = 0x0006

    RESET_EVENT_1           = 0x0010
    TRIGGER_EVENT_1         = 0x0020
    TRIGGER_RESET_EVENT_1   = 0x0030
    RESET_EVENT_2           = 0x0040
    TRIGGER_EVENT_2         = 0x0080
    TRIGGER_RESET_EVENT_2   = 0x00c0

    READ_SENSORS            = 0x0100
    LOG_SENSORS             = 0x0200
    CLEAR_FB_STATUS         = 0x4000
    BOOT_STRAP              = 0x8000


class BootStrapControl(Enum):
    WRITE_CMD = 0x1
    ERASE_CMD = 0x2
    READ_CMD = 0x4
    CHKSUM_CMD = 0x8
    RESET_CMD = 0x10
    INDEX_FAULT = 0x20
    COMMAND_FAULT = 0x40
    ADDRESS_FAULT = 0x80
    ANY_FAULT = 0xE0


class DataType(Enum):
    S8 = 0
    U8 = 1
    S16 = 2
    U16 = 3
    S32 = 4
    U32 = 5
    FLOAT = 6
    STRING = 7


class SensorType:
    class DigitalProbe(Enum):
        SENSE_ELEMENT_1 = 0x01
        SENSE_ELEMENT_2 = 0x02
        SENSE_ELEMENT_3 = 0x03
        SENSE_ELEMENT_4 = 0x04

    class Thermocouple(Enum):
        J = 0x00
        K = 0x01
        T = 0x02
        E = 0x03
        N = 0x04
        DIN_J = 0x05
        RO = 0x06
        S = 0x07
        B = 0x08
        C = 0x09

    class RTD(Enum):
        Type_385_100 = 0x00
        Type_385_500 = 0x01
        Type_385_1k = 0x02
        Type_392_100 = 0x03
        Type_3916_100 = 0x04

    class Process(Enum):
        Type_4_20_mA = 0x00
        Type_0_24_mA = 0x01
        Type_0_10_V = 0x02
        Type_0_1_V = 0x03
        Type_0_P1_V = 0x04
        Type_Plus_Minus_10_V = 0x05
        Type_Plus_Minus_1_V = 0x06
        Type_Plus_Minus_P1_V = 0x07
        Type_Plus_Minus_P05_V = 0x08
        Type_0_2_V = 0x09
        Type_Plus_Minus_2_V = 0x0a

    class DigitalIO(Enum):
        DIN = 0x00
        RATE = 0x01
        PULSE_WIDTH = 0x02
        DUTY_CYCLE = 0x03
        PULSE_DELAY = 0x04
        COUNTER = 0x05
        UP_DOWN_COUNTER = 0x06
        QUAD_COUNTER = 0x07

    class InvalidSensor(Enum):
        InvalidSensor = 0x00


class OutputType(Enum):
    NULL = 0
    PWM = 1
    Process = 2


class PwmConfig(Enum):
    Pwm_On_Off = 0b0000
    Pwm_point_1_s = 0b0001
    Pwm_1_s = 0b0010
    Pwm_10_s = 0b0011


class PwmPolarity(Enum):
    Active_High = 0
    Active_Low = 1


class FaultCode(Enum):
    # system error
    E_OK = 0x00
    E_BUSY = 0x80
    E_PARAMETER = 0x81
    E_SUPPORT = 0x82
    E_DEVICE = 0x83
    E_NACK = 0x84
    E_EMPTY = 0x85
    E_AVAILABLE = 0x86
    E_MEMORY = 0x87
    E_STATE = 0x88
    E_CONFIG = 0x89
    E_CHECKSUM = 0x8a
    E_WRITE = 0x8b
    E_POWER = 0xbc
    E_ADDRESS = 0xbd
    E_WAITDATA = 0x8e
    # system warning
    W_OVER_TEMP = 0x40
    W_OVER_VOLTAGE = 0x41
    # func block error
    E_BLOCK = 0x90
    E_OPERATION = 0x91
    E_OPERAND = 0x92
    E_STACK = 0x93
    E_OPERATOR = 0x94
    E_CONVERSION = 0x95
    E_SPECIALREG = 0x96
    E_EOF = 0xff
    E_OPEN = 0xfe
    E_CLOSE = 0xfd
    E_SEEK = 0xfc
    E_IOCTL_CMD = 0xfb
    E_SPACE = 0xfa
    E_HANDLE = 0xf9


class StringEscape(Enum):
    ENDOFSTRING = 0x00
    ESCAPE_CODE_MASK = 0x80
    SPECIFIC_CODE_MASK = 0x08  # if bit is set SPECIFIC escape code, otherwise it's a WIDTH_SHIFT code
    SHIFT_WIDTH_CODE = 0x81  # Used to flag byte as Shift_Width code

    FIELD_SHIFT_0 = 0x00  # Must be combined with FIELD_WIDTH
    FIELD_SHIFT_1 = 0x01
    FIELD_SHIFT_2 = 0x02
    FIELD_SHIFT_3 = 0x03
    FIELD_SHIFT_4 = 0x04
    FIELD_SHIFT_5 = 0x05
    FIELD_SHIFT_6 = 0x06
    FIELD_SHIFT_7 = 0x07
    FIELD_SHIFT_MASK = 0x07
    FIELD_SHIFT_SHIFT = 0x00

    FIELD_WIDTH_1 = 0x90  # shift limited to 0..7
    FIELD_WIDTH_2 = 0xa0
    FIELD_WIDTH_3 = 0xb0
    FIELD_WIDTH_4 = 0xc0
    FIELD_WIDTH_5 = 0xd0
    FIELD_WIDTH_6 = 0xe0
    FIELD_WIDTH_7 = 0xf0
    FIELD_WIDTH_MASK = 0x70
    FIELD_WIDTH_SHIFT = 0x04

    SENSOR_TYPE = 0x88  # Type(Range) of selected sensor
    SENSOR_CONFIG = 0x89  # Device Byte entries for selected sensor

    OUTPUT_TYPE = 0x8c  # Output type
    OUTPUT_CONFIG = 0x8e  # Configuration options for this output

    DEVICE_PARAMETER_0 = 0x98  # bottom 3 bits determines the Parameter
    DEVICE_PARAMETER_1 = 0x99
    DEVICE_PARAMETER_2 = 0x9a
    DEVICE_PARAMETER_3 = 0x9b
    DEVICE_PARAMETER_4 = 0x9c
    DEVICE_PARAMETER_5 = 0x9d
    DEVICE_PARAMETER_6 = 0x9e
    DEVICE_PARAMETER_7 = 0x9f

    PARAMETER_NAME = 0xa8
    FB_PARAMETER_NAME = 0xa9
    FB_NAME = 0xaa

    CONFIG_LIST = 0xfc  # list of available configurations
    DEVICE_NAME_STRING = 0xfd  # overall module type(ie: "ZW-ED")
    CALIBRATIONLIST = 0xfe  # Calibration entries
    ENDOFLIST = 0xff


class SensorDescriptor:
    def __init__(self):
        self.meas_type = MeasurementType.Error
        self.data_extended_function = 0
        self.data_factory_calibrate = 0
        self.data_config_descriptor = 0
        self.data_smartsensor = 0
        self.data_type = DataType.U8
        self.config_lock = 0
        self.config_scaling = 0
        self.config_assigned_channel = 0
        self.config_available = 0
        self.config_sensor_type = SensorType.InvalidSensor.InvalidSensor
        self.device_type = SensorDevice.NULL


class ListSelect:
    def __init__(self):
        self.list_select = 0
        self.block_select = 0


class Calibration:
    def __init__(self):
        self.active_segment = 0.0
        self.max_segment = 0.0
        self.polynomial_order = 0.0
        self.max_polynomial = 0.0
        self.inflection_point = 0.0
        self.offset = 0.0
        self.gain = 0.0


class SystemStatus:
    def __init__(self):
        self.device_locked = 0
        self.factory_access = 0
        self.device_ready = 0
        self.health_fault = 0
        self.sensor_fault = 0
        self.read_active = 0
        self.extract_valid = 0
        self.sensor_valid = 0
        self.system_fault = 0
        self.intr_active = 0
        self.device_reset = 0
        self.power_reset = 0
        self.sensor_bits = 0


class DataTime:
    def __init__(self):
        self.days = 0
        self.hours = 0
        self.mins = 0
        self.secs = 0


class R(Enum):
    DEVICE_ID = 'DEVICE_ID'
    FIRMARE_VERSION = 'FIRMARE_VERSION'
    HARDWARE_VERSION = 'HARDWARE_VERSION'
    SENSOR_LIST_SELECT = 'SENSOR_LIST_SELECT'
    BLOCK_OPTIONS = 'BLOCK_OPTIONS'
    OPERATING_HOURS = 'OPERATING_HOURS'
    EVENT_1_TIME_BASE = 'EVENT_1_TIME_BASE'
    EVENT_2_TIME_BASE = 'EVENT_2_TIME_BASE'
    SYSTEM_CONTROL = 'SYSTEM_CONTROL'
    INTERRUPT_STATUS = 'INTERRUPT_STATUS'
    INTERRUPT_CONTROL = 'INTERRUPT_CONTROL'
    NUMBER_OF_SENSORS = 'NUMBER_OF_SENSORS'
    NUMBER_OF_OUTPUTS = 'NUMBER_OF_OUTPUTS'
    OPERATING_TEMP = 'OPERATING_TEMP'
    OPERATING_VOLTAGE = 'OPERATING_VOLTAGE'
    FAULT_PROCESS = 'FAULT_PROCESS'
    FAULT_CODE = 'FAULT_CODE'
    EVENT_1_TIMER = 'EVENT_1_TIMER'
    EVENT_2_TIMER = 'EVENT_2_TIMER'
    SYSTEM_STATUS = 'SYSTEM_STATUS'
    TRIGGER_REQUESTS = 'TRIGGER_REQUESTS'
    EXTRACT_I2C_TIME = 'EXTRACT_I2C_TIME'
    EXTRACT_END_TIME = 'EXTRACT_END_TIME'

    NUMBER_OF_RECORDS = 'NUMBER_OF_RECORDS'
    CURRENT_TIME = 'CURRENT_TIME'
    SENSOR_1_DATA = 'SENSOR_1_DATA'
    SENSOR_2_DATA = 'SENSOR_2_DATA'
    SENSOR_3_DATA = 'SENSOR_3_DATA'
    SENSOR_4_DATA = 'SENSOR_4_DATA'
    EXTRACTED_TIME_STAMP = 'EXTRACTED_TIME_STAMP'
    SENSOR_1_EXTRACTED_DATA = 'SENSOR_1_EXTRACTED_DATA'
    SENSOR_2_EXTRACTED_DATA = 'SENSOR_2_EXTRACTED_DATA'
    SENSOR_3_EXTRACTED_DATA = 'SENSOR_3_EXTRACTED_DATA'
    SENSOR_4_EXTRACTED_DATA = 'SENSOR_4_EXTRACTED_DATA'

    SENSOR_1_DESCRIPTOR = 'SENSOR_1_DESCRIPTOR'
    SENSOR_2_DESCRIPTOR = 'SENSOR_2_DESCRIPTOR'
    SENSOR_3_DESCRIPTOR = 'SENSOR_3_DESCRIPTOR'
    SENSOR_4_DESCRIPTOR = 'SENSOR_4_DESCRIPTOR'

    SENSOR_1_OFFSET = 'SENSOR_1_OFFSET'
    SENSOR_2_OFFSET = 'SENSOR_2_OFFSET'
    SENSOR_3_OFFSET = 'SENSOR_3_OFFSET'
    SENSOR_4_OFFSET = 'SENSOR_4_OFFSET'

    SENSOR_1_GAIN = 'SENSOR_1_GAIN'
    SENSOR_2_GAIN = 'SENSOR_2_GAIN'
    SENSOR_3_GAIN = 'SENSOR_3_GAIN'
    SENSOR_4_GAIN = 'SENSOR_4_GAIN'

    SENSOR_1_UNIT = 'SENSOR_1_UNIT'
    SENSOR_2_UNIT = 'SENSOR_2_UNIT'
    SENSOR_3_UNIT = 'SENSOR_3_UNIT'
    SENSOR_4_UNIT = 'SENSOR_4_UNIT'

    DEVICE_NAME = 'DEVICE_NAME'

    OUTPUT_1 = 'OUTPUT_1'
    OUTPUT_2 = 'OUTPUT_2'
    OUTPUT_3 = 'OUTPUT_3'
    OUTPUT_4 = 'OUTPUT_4'


    # Manufacturing Register / May Require unlock

    MFR_DEVICE_ID = 'MFR_DEVICE_ID'
    MFR_HARDWARE_VERSION = 'MFR_HARDWARE_VERSION'
    MFR_CORE_FIRMWARE_VER = 'MFR_CORE_FIRMWARE_VER'
    MFR_BLOCK_I2C_RETRY = 'MFR_BLOCK_I2C_RETRY'
    MFR_RTC_CALIBRATION = 'MFR_RTC_CALIBRATION'
    MFR_FEATURE_BITS = 'MFR_FEATURE_BITS'
    MFR_DEFAULT_EVENT_1_TIME_BASE = 'MFR_DEFAULT_EVENT_1_TIME_BASE'
    MFR_DEFAULT_EVENT_2_TIME_BASE = 'MFR_DEFAULT_EVENT_2_TIME_BASE'
    MFR_SYSTEM_CONTROL = 'MFR_SYSTEM_CONTROL'
    MFR_SYSTEM_INTERRUPT = 'MFR_SYSTEM_INTERRUPT'
    MFR_SENSOR_LIST_INDEX = 'MFR_SENSOR_LIST_INDEX'
    MFR_SENSOR_LIST_SELECT = 'MFR_SENSOR_LIST_SELECT'

    MFR_ERROR_COUNT_1 = 'MFR_ERROR_COUNT_1'
    MFR_ERROR_COUNT_2 = 'MFR_ERROR_COUNT_2'
    MFR_ERROR_COUNT_3 = 'MFR_ERROR_COUNT_3'
    MFR_ERROR_COUNT_4 = 'MFR_ERROR_COUNT_4'
    MFR_MANUFACTURING_DATE = 'MFR_MANUFACTURING_DATE'
    MFR_CALIBRATION_DATE = 'MFR_CALIBRATION_DATE'
    MFR_OPERATING_TIME = 'MFR_OPERATING_TIME'
    MFR_CALIBRATION_TIME = 'MFR_CALIBRATION_TIME'
    MFR_OUTPUT_CONFIG_1 = 'MFR_OUTPUT_CONFIG_1'
    MFR_OUTPUT_CONFIG_2 = 'MFR_OUTPUT_CONFIG_2'
    MFR_OUTPUT_CONFIG_3 = 'MFR_OUTPUT_CONFIG_3'
    MFR_OUTPUT_CONFIG_4 = 'MFR_OUTPUT_CONFIG_4'

    #Calibration registers
    MFR_MSP430_CL_1 = 'MFR_MSP430_CL_1'
    MFR_MSP430_CL_2 = 'MFR_MSP430_CL_2'
    MFR_MSP430_V1_1 = 'MFR_MSP430_V1_1'
    MFR_MSP430_V1_2 = 'MFR_MSP430_V1_2'
    MFR_ADS1248_CL_1 = 'MFR_ADS1248_CL_1'
    MFR_ADS1248_CL_2 = 'MFR_ADS1248_CL_2'
    MFR_ADS1248_V1_1 = 'MFR_ADS1248_V1_1'
    MFR_ADS1248_V1_2 = 'MFR_ADS1248_V1_2'
    MFR_ADS1248_P1_1 = 'MFR_ADS1248_P1_1'
    MFR_ADS1248_P1_2 = 'MFR_ADS1248_P1_2'
    MFR_ADS1248_P05_1 = 'MFR_ADS1248_P05_1'
    MFR_ADS1248_P05_2 = 'MFR_ADS1248_P05_2'
    MFR_ADS1248_V10_1 = 'MFR_ADS1248_V10_1'
    MFR_ADS1248_V10_2 = 'MFR_ADS1248_V10_2'
    MFR_ADS_TC_1 = 'MFR_ADS_TC_1'
    MFR_ADS_TC_2 = 'MFR_ADS_TC_2'
    MFR_ADS_RTD_2W = 'MFR_ADS_RTD_2W'
    MFR_ADS_RTD_3W = 'MFR_ADS_RTD_3W'
    MFR_ADS_RTD_4W = 'MFR_ADS_RTD_4W'