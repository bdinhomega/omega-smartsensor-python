import time
from omegasensor import *


def get_readings(sensor: Smartsensor):
    print("Time: ", sensor.current_time_str())
    for i in range(4):
        print("%0.2f" % sensor.sensor_reading(i),
              " %s" % sensor.sensor_unit(i),
              "\t", end='')
    print('\n')


def example_callback(sensor, api_event: ApiEvent):
    if api_event == ApiEvent.API_SENSOR_ATTACHED:
        print("Sensor Attached!")
    if api_event == ApiEvent.API_SENSOR_DETACHED:
        print("Sensor Detached!")
    if api_event == ApiEvent.API_DATA_VALID:
        get_readings(sensor)


def main():
    # use Modbus interface
    # bus = BusModbus('/dev/ttyACM0', SMARTSENSOR_MODBUS_ADDR)

    # use I2C interface
    bus = BusI2C(3, SMARTSENSOR_I2C_ADDR)
    ss = Smartsensor(bus, 16, example_callback)

    ss.soft_reset()
    ss.preset_config()
    print("Firmware: 0x%08x" % ss.read(R.FIRMARE_VERSION))
    print("Device Id: 0x%08x" % ss.read(R.DEVICE_ID))
    print("Device name: %s" % ss.read(R.DEVICE_NAME))
    io_count = ss.read(R.IO_COUNT)
    print("On-board %d sensors" % io_count.sensors)
    print("On-board %d outputs" % io_count.outputs)

    ss.interrupt_enable = True
    while True:

        time.sleep(10)
        break


if __name__ == "__main__":
    main()
