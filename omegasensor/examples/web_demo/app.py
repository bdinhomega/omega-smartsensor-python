import time
from datetime import datetime
import logging
from flask import Flask, render_template
from flask_socketio import SocketIO
from omegasensor import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdefgh"
app.config['DEBUG'] = True
socketio = SocketIO(app)

nClients = 0


def example_callback(sensor, api_event: ApiEvent):
    if api_event == ApiEvent.API_SENSOR_ATTACHED:
        print("Sensor Attached!")
    if api_event == ApiEvent.API_SENSOR_DETACHED:
        print("Sensor Detached!")
    if api_event == ApiEvent.API_DATA_VALID:
        print("Time: ", sensor.current_time_str())
        io_count = ss.read(R.IO_COUNT)
        sensor_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(sensor_time)
        for i in range(io_count.sensors):
            socketio.emit("sensor_data", {
                "sensor_id": "sensor_%d" % i,
                "sensor_time": sensor_time,
                "sensor_value": sensor.sensor_reading(i),
            })


# use I2C interface
bus = BusI2C(3, SMARTSENSOR_I2C_ADDR)
ss = Smartsensor(bus, 16, example_callback)
ss.interrupt_enable = True


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    fw = ss.read(R.FIRMARE_VERSION)
    dev_id = ss.read(R.DEVICE_ID)
    dev_name = ss.read(R.DEVICE_NAME)
    io_count = ss.read(R.IO_COUNT)

    msg = {"Firmware": "%08X" % fw,
           "Device Id": "%08X" % dev_id,
           "Device Name": dev_name,
           "On-board sensor": io_count.sensors,
           "On-board output": io_count.outputs}
    socketio.emit("sensor_info", msg)

    for i in range(io_count.sensors):
        descriptor = ss.sensor_descriptor(i)
        print(descriptor.meas_type)
        unit_strings = {
            MeasurementType.Temperature_C: "Temperature",
            MeasurementType.Humidity_TH_percent: "Humidity",
            MeasurementType.Pressure: "Pressure",
            MeasurementType.Pressure_mbar: "Light",
            MeasurementType.DioType: "Digital"
        }
        sensor_meas = unit_strings.get(descriptor.meas_type, "Default")
        msg = {
            "sensor_id": "sensor_%d" % i,
            "sensor_meas": sensor_meas,
            "sensor_unit": ss.sensor_unit(i)
        }
        socketio.emit("new_sensor", msg)


@socketio.on('disconnect')
def on_disconnect():
    pass


def main():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    socketio.run(app, debug=False, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
