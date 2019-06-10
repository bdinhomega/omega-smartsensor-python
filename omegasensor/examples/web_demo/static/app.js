let socket;

$(document).ready( function() {
    colors = {
        "sensor_0": "bg-c-red",
        "sensor_1": "bg-c-green",
        "sensor_2": "bg-c-yellow",
        "sensor_3": "bg-c-blue"
    };
    socket = io.connect("http://" + document.domain + ":" + location.port);

    socket.on('connect', function () {
        console.log("connected")
    });
    socket.on('sensor_info', function (msg) {
        console.log("sensor_info", msg);
        content = "";
        for (var key in msg) {
            content += `<tr><td>${key}</td><td>${msg[key]}</td></tr>`
        }
        if ($('#idSensorInfo tbody').length === 0)
            $('#idSensorInfo').append("<tbody></tbody>");
        $('#idSensorInfo tbody').append(content);
    });
    socket.on('new_sensor', function (msg) {
        console.log("new_sensor", msg);
        color = colors[msg['sensor_id']];
        html = `
        <div id=${msg['sensor_id']} class="col-md-4 col-xl-3">
            <div class="card ${color} order-card">
                <div class="card-block">
                    <h5 class="m-b-20">${msg['sensor_meas']}</h5>
                    <h2 class="text-right"><i class="fa f-left"></i><span>---</span></h2>
                    <p class="m-b-0"><span class="f-left">---</span><span class="f-right">${msg['sensor_unit']}</span></p>
                </div>
            </div>
        </div>`;
        $("#idSensorRow").append(html);
    });
    socket.on('sensor_data', function (msg) {
        // console.log("sensor_data", msg);
        value = Math.round(msg['sensor_value'] * 100)/100;
        $("#" + msg["sensor_id"]).find("h2 span").text(value);
        $("#" + msg["sensor_id"]).find("p .f-left").text(msg['sensor_time']);
    });
});