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
}

$('#get_simulation_btn').on('click', function(ev) {
    SimulationId = $("#get_simulation_id")[0].value
    options = $("#get_simulation_content")[0].options
    content = []
    for (var i = 0; i < options.length; i++) {
        if (options[i].selected) {
            content.push(options[i].value)
        }
    }
    payload = {
        "SimulationId": SimulationId,
        "content": content,
        "anomalyDetection": 1
    }
    data = {
        "operation": "get_simulation",
        "payload": payload
    }
    $.ajax(ajaxSetting('', data)).done(function(response) {
        $("#response")[0].innerHTML = JSON.stringify(response, null, 4)

        item = content[0]
        supported_graph = ["Speed", "Direction", "ServoAngle", "EngineTemperature", "RPM"]
        if (supported_graph.indexOf(item) != -1) {
            $("#graph")[0].style.display = "block"
            graphData = []
            graphLabels = []
            for (i = 0; i < response[item]["value"].length; i++) {
                graphData.push(
                    parseInt(response[item]["value"][i])
                )
                graphLabels.push(response[item]["time"][i])
            }
            const datapoints = {
                labels: graphLabels,
                datasets: [{
                    label: item,
                    data: graphData,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            };
            const config = {
                type: 'line',
                data: datapoints,
            };
            const myChart = new Chart(
                "graph",
                config
            );
        } else {
            $("#graph")[0].style.display = "none"
        }
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
