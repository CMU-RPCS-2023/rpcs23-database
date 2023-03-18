SERVER = 'https://fwo91hdzog.execute-api.us-east-1.amazonaws.com/test/dynamodbmanager'

function ajaxSetting(api, data) {
    setting = {
        "async": true,
        "crossDomain": true,
        "url": SERVER + api,
        "method": "POST",
        "headers": {
            "content-type": "application/json",
        },
        "processData": false,
        "data": JSON.stringify(data),
        "cors": true
    }
    return setting
}

window.onload = function ()
{
    const data = {
        'operation': 'echo',
        'payload': 'server is ok'
    };
    $.ajax(ajaxSetting('', data)).done(function(response) {
        console.log(response)
        if (response !== 'server is ok') {
            document.getElementById('server-check-warning').style.display = 'block'
        }
    }).catch(function(error) {
        console.log(error)
        document.getElementById('server-check-warning').style.display = 'block'
    })

    $("#add_simulation")[0].value = JSON.stringify({
        "id": "Test123",
        "SimulationId": "Test123",
        "SimulationName": "Test Simulation Created by Jhao-Ting Chen",
        "StartTime": "2023-03-17T00:52:14",
        "EndTime": "2023-03-18T00:52:14",        
        "CarId": "Tesla",
        "TrackId": "easy1",
        "SensorLog": [
            {
                "Timestamp": "2023-03-17T15:23:14",
                "SensorType": "GPS",
                "Value": {"Lat": 22.3, "Lng": 12.32}
            }
        ],
        "CarLog": [
            {
                "Timestamp": "2023-03-17T15:23:14",
                "CarStatus": "on",
                "Speed": 43,
                "Position": {
                    "x": 12.3,
                    "y": 12.3,
                    "z": 12.3
                },
                "Yaw": {
                    "x": 12.3,
                    "y": 12.3,
                    "z": 12.3
                },
                "Pitch": {
                    "x": 12.3,
                    "y": 12.3,
                    "z": 12.3
                },
                "Roll": {
                    "x": 12.3,
                    "y": 12.3,
                    "z": 12.3
                },
                "Accel": {
                    "x": 12.3,
                    "y": 12.3,
                    "z": 12.3
                },
                "Direction": 180,
                "ServoAngle": 56,
                "EngineTemperature": 72,
                "RPM": 30
            }
        ],
        "EventLog": [
            {
                "Timestamp": "2023-03-17T15:23:14",
                "EventType": "Collision",
                "Risk": 2,
                "ErrorMessage": "Hit a Tree"
            }
        ],
    }, null, 4)
    $("#get_simulation")[0].value = JSON.stringify({
        "SimulationId": "Test123",
    })
    $("#delete_simulation")[0].value = JSON.stringify({
        "SimulationId": "Test123",
    })
}

$('#get_simulation_btn').on('click', function(ev) {
    payload = JSON.parse($("#get_simulation")[0].value)
    data = {
        "operation": "get_simulation",
        "payload": payload
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#add_simulation_btn').on('click', function(ev) {
    payload = JSON.parse($("#add_simulation")[0].value)
    data = {
        "operation": "add_simulation",
        "payload": JSON.parse($("#add_simulation")[0].value)
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})

$('#delete_simulation_btn').on('click', function(ev) {
    payload = JSON.parse($("#delete_simulation")[0].value)
    data = {
        "operation": "delete_simulation",
        "payload": payload
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)
    })
})


function addAlert(content, type) {
    alertID = Date.now()
    clearTimeout(timeout)

    // add an alert to #alertBox
    document.getElementById("alertBox").innerHTML += `
        <div class="alert alert-` + type + ` alert-dismissible fade show JobAdded" role="alert" id="` + alertID + `">
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
            ` + content + `
        </div>
    `;

    timeout = setTimeout(() => { $(`.JobAdded`).alert('close') }, 3000);
}
