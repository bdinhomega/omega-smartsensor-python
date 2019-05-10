import logging
import time
from .smartsensor import Device
from .registers import *
from .bus import Bus


class Smartsensor:
    def __init__(self, transport: Bus):
        """
            Initialize interface for Smartsensor device with the provided transport
        :param transport: bus transport
        """
        assert(isinstance(transport, Bus))
        self.ss = Device(transport)

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
        self.ss.write(R.EVENT_1_TIME_BASE, 1)
        self.ss.write(R.INTERRUPT_CONTROL, 0)
        self.ss.write(R.SYSTEM_CONTROL,
                      SystemControl.ENABLE_SENSOR_CHANGE_LOG |
                      SystemControl.ENABLE_POWER_CHANGE_LOG |
                      SystemControl.ENABLE_HEALTH_FAULT_LOG |
                      SystemControl.ENABLE_TIME_CHANGE_LOG |
                      SystemControl.ENABLE_EVENT_1_READ |
                      SystemControl.ENABLE_EVENT_1_LOG |
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
        return self.ss.read([R.SENSOR_1_DATA, R.SENSOR_2_DATA,
                             R.SENSOR_3_DATA, R.SENSOR_4_DATA][sensor_num])

    def sensor_unit(self, sensor_num) -> str:
        """
            Get sensor unit
        :param sensor_num: index
        :return: unit in string
        """
        return self.ss.read([R.SENSOR_1_UNIT, R.SENSOR_2_UNIT,
                             R.SENSOR_3_UNIT, R.SENSOR_4_UNIT][sensor_num])

    def sensor_descriptor(self, sensor_num) -> SensorDescriptor:
        """
            Get sensor descriptor
        :param sensor_num: index
        :return: sensor descriptor
        """
        return self.ss.read([R.SENSOR_1_DESCRIPTOR, R.SENSOR_2_DESCRIPTOR,
                             R.SENSOR_3_DESCRIPTOR, R.SENSOR_4_DESCRIPTOR][sensor_num])

    def sensor_type(self, sensor_num) -> MeasurementType:
        """
            Get sensor type
        :param sensor_num: index
        :return: measurement type
        """
        return self.sensor_descriptor(sensor_num).meas_type

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

