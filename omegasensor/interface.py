import logging
import time
from .smartsensor import Device, DeviceType
from .registers import *
from .bus import Bus


class Smartsensor:
    def __init__(self, transport: Bus,
                 interrupt_pin: int = None,
                 interrupt_callback = None):
        """
            Initialize interface for Smartsensor device with the provided transport
        :param transport: bus transport
        :param interrupt_pin: specify the pin number (BCM pin for Rpi).
        If None, interrupt processing will be disabled.
        :param interrupt_callback: specify user callback function to be notified when
        an event is signaled from the smartsensor.
        If None, interrupt processing will be disabled.

        @interrupt_enable attribute if disabled will mask interrupt processing events
            and if enabled will allow user interrupt callback
        """
        assert(isinstance(transport, Bus))
        # provide some initial configuration
        self.config = {}
        self.config['HEARTBEAT_MAX_MISS'] = 3
        self.user_callback = interrupt_callback
        self.interrupt_enable = False
        self.ss = Device(transport,
                         interrupt_pin,
                         self._user_callback,
                         self.config)

    def _user_callback(self, event: ApiEvent):
        """
            This callback will invoke user callback, it will also
            pass "this instance" as first param.
        :param event: ApiEvent that the interrupt raises
        :return: None
        """
        if self.interrupt_enable and self.user_callback:
            self.user_callback(self, event)

    def read(self, register: R):
        """
            Read from smartsensor register
        :param register: smartsensor register
        :return: data
        """
        return self.ss.read(register)

    def write(self, register: R, value):
        """
            Write to smartsensor register
        :param register: smartsensor register
        :param value: value
        """
        self.ss.write(register, value)

    def preset_config(self):
        """
            Configure sensor for Basic configuration for most application
        """
        self.ss.write(R.EVENT_0_TIME_BASE, 1)
        self.ss.write(R.INTERRUPT_CONTROL,
                      InterruptEnable.INTR_DATA_READY |
                      InterruptEnable.INTR_SENSOR_CHANGE |
                      InterruptEnable.INTR_POWER_CHANGE |
                      InterruptEnable.INTR_HEALTH_CHANGE)
        self.ss.write(R.SYSTEM_CONTROL,
                      SystemControl.ENABLE_SENSOR_CHANGE_LOG |
                      SystemControl.ENABLE_POWER_CHANGE_LOG |
                      SystemControl.ENABLE_HEALTH_FAULT_LOG |
                      SystemControl.ENABLE_TIME_CHANGE_LOG |
                      SystemControl.ENABLE_EVENT_0_READ |
                      SystemControl.ENABLE_EVENT_0_LOG |
                      SystemControl.ENABLE_FUNCTION_BLOCK |
                      SystemControl.ENABLE_HEALTH_MONITOR |
                      SystemControl.ENABLE_LOG_OVERWRITE |
                      SystemControl.ENABLE_RTC)

    def wait_system_ready(self, max_wait=3):
        """
            Poll sensor until it is ready, optional timeout value
        :param max_wait: timeout in seconds
        """
        wait_time = 0.2
        s = SystemStatus()
        while max_wait > 0:
            try:
                s = self.ss.read(R.SYSTEM_STATUS)
                if s.device_ready:
                    break
            except:
                pass
            time.sleep(wait_time)
            max_wait -= wait_time
        logging.debug("wait_system_ready, device_ready = %d" % s.device_ready)

    def soft_reset(self):
        """
            Soft Reset the sensor
        """
        self.ss.write(R.TRIGGER_REQUESTS, Trigger.DEVICE_RESET)
        self.wait_system_ready()

    def factory_reset(self):
        """
            Factory reset the sensor
        """
        self.ss.write(R.TRIGGER_REQUESTS, Trigger.FACTORY_RESET)
        self.wait_system_ready()

    def current_time_str(self) -> str:
        """
            Get formatted current time stamp from sensor
        :return: formatted timestamp in string
        """
        t = self.ss.read(R.CURRENT_TIME)
        return "%d days %d hours %d mins %d secs" % (t.days, t.hours, t.mins, t.secs)

    def current_time(self) -> DataTime:
        """
            Get current time stamp from sensor
        :return: DataTime timestamp
        """
        t = self.ss.read(R.CURRENT_TIME)
        return t

    def sensor_reading(self, sensor_num) -> float:
        """
            Get sensor reading
        :param sensor_num: index
        :return: sensor reading in float
        """
        return self.ss.read([R.SENSOR_0_DATA, R.SENSOR_1_DATA,
                             R.SENSOR_2_DATA, R.SENSOR_3_DATA][sensor_num])

    def sensor_unit(self, sensor_num) -> str:
        """
            Get sensor unit
        :param sensor_num: index
        :return: unit in string
        """
        return self.ss.read([R.SENSOR_0_UNIT, R.SENSOR_1_UNIT,
                             R.SENSOR_2_UNIT, R.SENSOR_3_UNIT][sensor_num])

    def sensor_descriptor(self, sensor_num) -> SensorDescriptor:
        """
            Get sensor descriptor
        :param sensor_num: index
        :return: sensor descriptor
        """
        return self.ss.read([R.SENSOR_0_DESCRIPTOR, R.SENSOR_1_DESCRIPTOR,
                             R.SENSOR_2_DESCRIPTOR, R.SENSOR_3_DESCRIPTOR][sensor_num])

    def sensor_type(self, sensor_num) -> MeasurementType:
        """
            Get sensor type
        :param sensor_num: index
        :return: measurement type
        """
        return self.sensor_descriptor(sensor_num).meas_type

    def get_sensor_digital_device_type(self, sensor_num) -> DigitalInputDeviceByte:
        """Gets the device type byte and unpacks it into reset, enable and clock fields,
            For devices that have these fields.
        :param sensor_num: index of sensor
        :return: object with reset,enable and clock members
        """

        device_type_byte= DeviceType()

        return device_type_byte.unpack(self.sensor_descriptor(sensor_num).device_type)

    def set_senor_digital_device_type(self, sensor_num, device_type:DigitalInputDeviceByte):
        """ Packs the fields reset,enable and clock back into one byte.
        Sets and writes the device type in the selected sensor descriptor. The descriptor
        assumes a sensor type of DIGITAL IO. Below is a snippet of how to use this method

        device_byte=ss.get_sensor_digital_device_type(0)
        device_byte.reset=InputDeviceByte.I_O_SIGNAL.N_O_SOURCE
        device_byte.enable = InputDeviceByte.I_O_SIGNAL.N_C_SOURCE
        device_byte.clock = InputDeviceByte.I_O_SIGNAL.N_C_SINK
        ss.set_senor_digital_device_type(0,device_byte)
        ss.soft_reset()

        :param sensor_num: index of sensor
        :param device_type_byte: object with reset,enable and clock members
        :return: void
        """
        device_type_byte = DeviceType()
        descriptor = self.sensor_descriptor(sensor_num)
        descriptor.device_type=device_type_byte.pack(device_type)
        descriptor.config_sensor_type = SensorType.DigitalIO(descriptor.config_sensor_type)
        self.write([R.SENSOR_0_DESCRIPTOR, R.SENSOR_1_DESCRIPTOR,
                             R.SENSOR_2_DESCRIPTOR, R.SENSOR_3_DESCRIPTOR][sensor_num],descriptor)


    def system_status(self) -> SystemStatus:
        """
            Get system status
        :return: Systems status
        """
        return self.ss.read(R.SYSTEM_STATUS)

    def set_trigger(self, trigger: Trigger):
        """
            Configure sensor's trigger request
        :param trigger: triggers
        """
        self.ss.write(R.TRIGGER_REQUESTS, trigger)

    def set_interrupt(self, interrupt: InterruptEnable):
        """
            Configure sensor's interrupt enables
        :param interrupt: interrupts
        """
        self.ss.write(R.INTERRUPT_CONTROL, interrupt)

    def set_system_ctrl(self, ctrl: SystemControl):
        """
            Configure sensor's system control
        :param ctrl: controls
        """
        self.ss.write(R.SYSTEM_CONTROL, ctrl)

