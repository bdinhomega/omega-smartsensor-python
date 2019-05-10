import time
from omegasensor import *


def main():
    bus = BusModbus('/dev/ttyACM0', SMARTSENSOR_MODBUS_ADDR)
    ss = Smartsensor(bus)

    ss.soft_reset()
    ss.preset_config()
    print("Firmware 0x%08x" % ss.read(R.FIRMARE_VERSION))
    print("Device Id 0x%08x" % ss.read(R.DEVICE_ID))
    print("Device %s" % ss.read(R.DEVICE_NAME))
    sensor_cnt = ss.read(R.NUMBER_OF_SENSORS)
    print("Onboard %d sensors" % sensor_cnt)
    print("Onboard %d outputs" % ss.read(R.NUMBER_OF_OUTPUTS))

    sensor_units = [ss.sensor_unit(i) for i in range(sensor_cnt)]

    while True:
        print("Time: ", ss.current_time_str())
        for i in range(sensor_cnt):
            print("%0.2f" % ss.sensor_reading(i),
                  " %s" % sensor_units[i],
                  "\t", end='')
        print('\n')
        time.sleep(1)


if __name__ == "__main__":
    main()