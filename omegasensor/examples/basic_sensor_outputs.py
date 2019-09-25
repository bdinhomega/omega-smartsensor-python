import time
from omegasensor import *


def main():
    # use Modbus interface
    bus = BusModbus('COM19', SMARTSENSOR_MODBUS_ADDR)

    # use I2C interface
    #bus = BusI2C(3, SMARTSENSOR_I2C_ADDR)
    ss = Smartsensor(bus)

    ss.soft_reset()
    ss.preset_config()
    print("Firmware: 0x%08x" % ss.read(R.FIRMARE_VERSION))
    print("Device Id: 0x%08x" % ss.read(R.DEVICE_ID))
    print("Device name: %s" % ss.read(R.DEVICE_NAME))
    io_count = ss.read(R.IO_COUNT)
    print("On-board %d sensors" % io_count.sensors)
    print("On-board %d outputs" % io_count.outputs)

    sensor_units = [ss.sensor_unit(i) for i in range(io_count.sensors)]
    sensor_outputs = [R.OUTPUT_0, R.OUTPUT_1]
    while True:
        print("Time: ", ss.current_time_str())
        for i in range(io_count.sensors):
            print("%0.2f" % ss.sensor_reading(i),
                  " %s" % sensor_units[i],
                  "\t", end='')
        print('\n')
        for i in range(io_count.outputs):
            ss.write(sensor_outputs[i],100)
            time.sleep(1)
            ss.write(sensor_outputs[i],0)
            time.sleep(1)



if __name__ == "__main__":
    main()
